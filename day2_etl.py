import pandas as pd
import glob
import os
from sqlalchemy import create_engine
import numpy as np

def find_amount_col(df):
    """Finds the column representing transaction amount regardless of naming variations."""
    for col in df.columns:
        if 'amount' in col:
            return col
    raise KeyError(f"Could not find an 'amount' column. Available columns: {list(df.columns)}")

def clean_data():
    os.makedirs("data/processed", exist_ok=True)
    
    print("Cleaning nav_history...")
    nav_df = pd.read_csv("data/raw/02_nav_history.csv")
    nav_df.columns = nav_df.columns.str.strip().str.lower()
    
    nav_df['date'] = pd.to_datetime(nav_df['date'], errors='coerce')
    nav_df = nav_df.sort_values(by=['amfi_code', 'date'])
    nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].ffill()
    nav_df = nav_df.drop_duplicates()
    nav_df = nav_df[nav_df['nav'] > 0]
    nav_df.to_csv("data/processed/nav_history_clean.csv", index=False)

    print("Cleaning investor_transactions...")
    txn_df = pd.read_csv("data/raw/08_investor_transactions.csv")
    txn_df.columns = txn_df.columns.str.strip().str.lower()
    
    amt_col = find_amount_col(txn_df)
    
    if 'transaction_type' in txn_df.columns:
        txn_df['transaction_type'] = txn_df['transaction_type'].astype(str).str.upper().str.strip()
        txn_df['transaction_type'] = txn_df['transaction_type'].replace(
            {'LUMP SUM': 'LUMPSUM', 'RED': 'REDEMPTION'}
        )
        
    txn_df[amt_col] = pd.to_numeric(txn_df[amt_col], errors='coerce')
    txn_df = txn_df[txn_df[amt_col] > 0]
    
    if 'date' in txn_df.columns:
        txn_df['date'] = pd.to_datetime(txn_df['date'], errors='coerce')
        
    if 'kyc_status' in txn_df.columns:
        valid_kyc = ['VERIFIED', 'PENDING', 'REJECTED']
        txn_df = txn_df[txn_df['kyc_status'].astype(str).str.upper().isin(valid_kyc)]
        
    txn_df.to_csv("data/processed/investor_transactions_clean.csv", index=False)

    print("Cleaning scheme_performance...")
    perf_df = pd.read_csv("data/raw/07_scheme_performance.csv")
    perf_df.columns = perf_df.columns.str.strip().str.lower()
    
    for col in ['1yr_return', '3yr_return', '5yr_return']:
        if col in perf_df.columns:
            perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce')
    
    if '1yr_return' in perf_df.columns:
        perf_df['anomaly_flag'] = np.where(
            (perf_df['1yr_return'] > 200) | (perf_df['1yr_return'] < -90), 1, 0
        )
    else:
        perf_df['anomaly_flag'] = 0
        
    if 'expense_ratio' in perf_df.columns:
        perf_df = perf_df[(perf_df['expense_ratio'] >= 0.1) & (perf_df['expense_ratio'] <= 2.5)]
        
    perf_df.to_csv("data/processed/scheme_performance_clean.csv", index=False)


    processed_files = ['02_nav_history', '08_investor_transactions', '07_scheme_performance']
    raw_csvs = glob.glob("data/raw/*.csv")
    
    for file in raw_csvs:
        filename = os.path.basename(file).replace('.csv', '')
        if not any(pf in filename for pf in processed_files):
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.lower()
            clean_name = filename.split('_', 1)[-1] if filename[0].isdigit() else filename
            df.to_csv(f"data/processed/{clean_name}_clean.csv", index=False)
            print(f"Passed through {filename} as {clean_name}_clean.csv")

def load_to_sqlite():
    print("\nLoading data into SQLite database (bluestock_mf.db)...")
    engine = create_engine('sqlite:///bluestock_mf.db')
    processed_csvs = glob.glob("data/processed/*.csv")
    
    for file in processed_csvs:
        table_name = os.path.basename(file).replace('_clean.csv', '')
        df = pd.read_csv(file)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        loaded_df = pd.read_sql(f"SELECT COUNT(*) as count FROM '{table_name}'", engine)
        print(f"Table '{table_name}' loaded with {loaded_df.iloc[0]['count']} rows.")

if __name__ == "__main__":
    clean_data()
    load_to_sqlite()