import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

def calculate_performance_metrics():
    conn = sqlite3.connect(DB_PATH)
    
    df_nav = pd.read_sql("SELECT * FROM nav_history", conn)
    
    # Case-insensitive column matching
    cols_lower = {c.lower(): c for c in df_nav.columns}
    nav_col = cols_lower.get('nav')
    date_col = cols_lower.get('date')
    group_col = cols_lower.get('amfi code') or cols_lower.get('amfi_code') or cols_lower.get('scheme code') or list(df_nav.columns)[0]

    if df_nav.empty or not nav_col:
        print("NAV data missing or incomplete in database.")
        conn.close()
        return

    df_nav[date_col] = pd.to_datetime(df_nav[date_col])
    df_nav[nav_col] = pd.to_numeric(df_nav[nav_col], errors='coerce')
    metrics_list = []

    for scheme_code, group in df_nav.groupby(group_col):
        group = group.sort_values(date_col).dropna(subset=[nav_col])
        if len(group) < 10:
            continue
            
        group['Daily_Return'] = group[nav_col].pct_change()
        
        n_days = len(group)
        start_val = group[nav_col].iloc[0]
        end_val = group[nav_col].iloc[-1]
        
        # 252 Trading Days CAGR
        cagr = ((end_val / start_val) ** (252 / n_days)) - 1 if start_val > 0 else 0
        
        annualized_vol = group['Daily_Return'].std() * np.sqrt(252)
        rf_rate = 0.065
        sharpe = (cagr - rf_rate) / annualized_vol if (annualized_vol and annualized_vol != 0) else np.nan
        
        var_95 = np.percentile(group['Daily_Return'].dropna(), 5) if len(group['Daily_Return'].dropna()) > 5 else 0
        
        metrics_list.append({
            'Amfi Code': scheme_code,
            'CAGR_Annualized': round(cagr * 100, 2),
            'Annualized_Vol': round(annualized_vol * 100, 2),
            'Sharpe_Ratio': round(sharpe, 2),
            'Historical_VaR_95': round(var_95 * 100, 2)
        })

    df_metrics = pd.DataFrame(metrics_list)
    df_metrics.to_csv(PROCESSED_DIR / "calculated_performance_metrics.csv", index=False)
    df_metrics.to_sql("calculated_performance_metrics", conn, if_exists="replace", index=False)
    conn.close()
    print("Performance metrics successfully computed and stored in SQLite.")

if __name__ == "__main__":
    calculate_performance_metrics()
