import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"

def run_etl():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    logging.info("Connected to SQLite Database.")

    # Helper function to find matching files
    def get_file(patterns):
        for p in patterns:
            matches = list(RAW_DIR.glob(p))
            if matches:
                return matches[0]
        return None

    # 1. Scheme Performance
    scheme_file = get_file(["*scheme_performance*.csv", "*07_scheme_performance*.csv"])
    if scheme_file:
        df_scheme = pd.read_csv(scheme_file)
        cols_to_clean = ['Aum Crore', 'Expense Ratio', 'Cagr 1yr', 'Cagr 3yr', 'Cagr 5yr', 'Sharpe Ratio', 'Beta']
        for col in cols_to_clean:
            for c in df_scheme.columns:
                if c.lower() == col.lower():
                    df_scheme[c] = pd.to_numeric(df_scheme[c].astype(str).str.replace('%', '').str.replace(',', ''), errors='coerce')
        df_scheme.to_csv(PROCESSED_DIR / "scheme_performance_clean.csv", index=False)
        df_scheme.to_sql("scheme_performance", conn, if_exists="replace", index=False)
        logging.info("Processed: scheme_performance")

    # 2. NAV History (Supports nav_history.csv or individual nav_*.csv files)
    nav_files = list(RAW_DIR.glob("*nav*.csv"))
    if nav_files:
        df_list = []
        for f in nav_files:
            try:
                temp_df = pd.read_csv(f)
                df_list.append(temp_df)
            except Exception as e:
                logging.warning(f"Could not read {f}: {e}")
        
        if df_list:
            df_nav = pd.concat(df_list, ignore_index=True)
            
            # Standardize column headers
            col_map = {c: c.strip().title() for c in df_nav.columns}
            df_nav = df_nav.rename(columns=col_map)
            
            # Fix case differences for standard columns
            for col in df_nav.columns:
                if col.lower() in ['nav', 'nav_value']:
                    df_nav = df_nav.rename(columns={col: 'Nav'})
                elif col.lower() in ['date', 'nav_date', 'transaction date']:
                    df_nav = df_nav.rename(columns={col: 'Date'})
                elif col.lower() in ['amfi code', 'amfi_code', 'scheme_code', 'scheme code']:
                    df_nav = df_nav.rename(columns={col: 'Amfi Code'})

            if 'Date' in df_nav.columns and 'Nav' in df_nav.columns:
                df_nav['Date'] = pd.to_datetime(df_nav['Date'], errors='coerce')
                df_nav['Nav'] = pd.to_numeric(df_nav['Nav'], errors='coerce')
                df_nav = df_nav.dropna(subset=['Date', 'Nav']).sort_values('Date')
                
                group_col = 'Amfi Code' if 'Amfi Code' in df_nav.columns else df_nav.columns[0]
                df_nav['Nav'] = df_nav.groupby(group_col)['Nav'].ffill()
                
                df_nav.to_csv(PROCESSED_DIR / "nav_history_clean.csv", index=False)
                df_nav.to_sql("nav_history", conn, if_exists="replace", index=False)
                logging.info(f"Processed: nav_history ({len(df_nav)} rows loaded)")

    # 3. Investor Transactions
    tx_file = get_file(["*investor_transactions*.csv", "*08_investor_transactions*.csv"])
    if tx_file:
        df_tx = pd.read_csv(tx_file)
        df_tx.to_csv(PROCESSED_DIR / "investor_transactions_clean.csv", index=False)
        df_tx.to_sql("investor_transactions", conn, if_exists="replace", index=False)
        logging.info("Processed: investor_transactions")

    # 4. Monthly SIP Inflows
    sip_file = get_file(["*monthly_sip_inflows*.csv", "*04_monthly_sip_inflows*.csv"])
    if sip_file:
        df_sip = pd.read_csv(sip_file)
        df_sip.to_csv(PROCESSED_DIR / "monthly_sip_inflows_clean.csv", index=False)
        df_sip.to_sql("monthly_sip_inflows", conn, if_exists="replace", index=False)
        logging.info("Processed: monthly_sip_inflows")

    conn.close()
    logging.info("ETL Pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()
