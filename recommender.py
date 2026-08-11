import argparse
import pandas as pd
import os

def load_scorecard():
    if os.path.exists("fund_scorecard.csv"):
        df = pd.read_csv("fund_scorecard.csv")
        df['amfi_code'] = df['amfi_code'].astype(str)
        return df
    else:
        print("⚠️ Notice: fund_scorecard.csv not found. Using dummy scorecard for testing.")
        return pd.DataFrame({
            'amfi_code': [f"1000{i}" for i in range(1, 6)],
            'scheme_name': [f"Equity Fund {chr(65+i)}" for i in range(5)],
            'sharpe_ratio': [1.45, 1.12, 0.95, 0.78, 0.62],
            'cagr_3yr': [18.2, 15.4, 12.1, 9.8, 7.5],
            'risk_grade': ['Low', 'Low', 'Moderate', 'High', 'High']
        })

def recommend_funds(risk_appetite):
    df = load_scorecard()
    if df is None or df.empty:
        print("❌ No data available for recommendations.")
        return

    if 'risk_grade' not in df.columns:
        def assign_risk(row):
            sharpe = row.get('sharpe_ratio', 1.0)
            if sharpe > 1.2:
                return 'Low'
            elif sharpe > 0.8:
                return 'Moderate'
            else:
                return 'High'
        df['risk_grade'] = df.apply(assign_risk, axis=1)

    appetite = risk_appetite.capitalize()
    filtered = df[df['risk_grade'] == appetite]
    
    if filtered.empty:
        filtered = df

    sort_col = 'sharpe_ratio' if 'sharpe_ratio' in filtered.columns else filtered.columns[0]
    top_3 = filtered.sort_values(by=sort_col, ascending=False).head(3)

    print(f"\n🎯 Top Fund Recommendations for [{appetite} Risk Appetite]:")
    print("=" * 75)
    cols = ['amfi_code', 'scheme_name', 'sharpe_ratio', 'cagr_3yr', 'risk_grade']
    display_cols = [c for c in cols if c in top_3.columns]
    if not display_cols:
        display_cols = top_3.columns[:4].tolist()
    print(top_3[display_cols].to_string(index=False))
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mutual Fund Recommendation Engine")
    parser.add_argument("--risk", type=str, default="Moderate", choices=["Low", "Moderate", "High"], help="User Risk Appetite")
    args = parser.parse_args()
    recommend_funds(args.risk)
