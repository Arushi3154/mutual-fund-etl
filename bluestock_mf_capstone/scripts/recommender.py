import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def generate_recommendations(top_n=5):
    conn = sqlite3.connect(DB_PATH)
    
    try:
        df_sp = pd.read_sql("SELECT * FROM scheme_performance", conn)
    except Exception:
        df_sp = pd.DataFrame()

    try:
        df_cp = pd.read_sql("SELECT * FROM calculated_performance_metrics", conn)
    except Exception:
        df_cp = pd.DataFrame()

    if df_sp.empty and df_cp.empty:
        print("No performance tables found in SQLite database.")
        conn.close()
        return

    if not df_sp.empty and not df_cp.empty:
        sp_amfi = [c for c in df_sp.columns if c.lower() in ['amfi code', 'amfi_code', 'scheme_code']][0]
        cp_amfi = [c for c in df_cp.columns if c.lower() in ['amfi code', 'amfi_code', 'scheme_code']][0]
        df = pd.merge(df_sp, df_cp, left_on=sp_amfi, right_on=cp_amfi, how='outer', suffixes=('_sp', '_cp'))
    else:
        df = df_sp if not df_sp.empty else df_cp

    def find_col(possible_names):
        for p in possible_names:
            for c in df.columns:
                if c.lower().strip() == p.lower().strip():
                    return c
        return None

    sharpe_col = find_col(['sharpe_ratio', 'sharpe ratio', 'sharpe_ratio_cp', 'sharpe_ratio_sp', 'sharpe'])
    cagr_col = find_col(['cagr_annualized', 'cagr 3yr', 'cagr_3yr', 'cagr_1yr', 'cagr_5yr', 'cagr'])
    name_col = find_col(['scheme name', 'scheme_name', 'scheme_name_sp', 'scheme_name_cp'])
    category_col = find_col(['category', 'category_sp', 'category_cp', 'scheme_category'])
    amfi_col = find_col(['amfi code', 'amfi_code', 'scheme_code', 'amfi_code_sp', 'amfi_code_cp'])

    df['Sharpe_Val'] = pd.to_numeric(df[sharpe_col], errors='coerce').fillna(0) if sharpe_col else 0.0
    df['CAGR_Val'] = pd.to_numeric(df[cagr_col], errors='coerce').fillna(0) if cagr_col else 0.0
    df['Score'] = (df['Sharpe_Val'] * 0.6) + (df['CAGR_Val'] * 0.4)

    df_sorted = df.sort_values(by='Score', ascending=False).head(top_n)

    out_df = pd.DataFrame()
    if amfi_col: out_df['Amfi_Code'] = df_sorted[amfi_col]
    if name_col: out_df['Scheme_Name'] = df_sorted[name_col]
    if category_col: out_df['Category'] = df_sorted[category_col]
    out_df['Sharpe_Ratio'] = df_sorted['Sharpe_Val']
    out_df['CAGR'] = df_sorted['CAGR_Val']
    out_df['Score'] = df_sorted['Score']

    out_df.to_csv(PROCESSED_DIR / "recommended_funds.csv", index=False)
    out_df.to_sql("recommended_funds", conn, if_exists="replace", index=False)
    conn.close()
    
    print(f"Top {top_n} Fund Recommendations Generated:")
    print(out_df.to_string(index=False))

if __name__ == "__main__":
    generate_recommendations()
