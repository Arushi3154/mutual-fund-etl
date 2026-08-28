CREATE TABLE IF NOT EXISTS "scheme_performance" (
"amfi_code" INTEGER,
  "scheme_name" TEXT,
  "fund_house" TEXT,
  "category" TEXT,
  "plan" TEXT,
  "return_1yr_pct" REAL,
  "return_3yr_pct" REAL,
  "return_5yr_pct" REAL,
  "benchmark_3yr_pct" REAL,
  "alpha" REAL,
  "beta" REAL,
  "sharpe_ratio" REAL,
  "sortino_ratio" REAL,
  "std_dev_ann_pct" REAL,
  "max_drawdown_pct" REAL,
  "aum_crore" INTEGER,
  "expense_ratio_pct" REAL,
  "morningstar_rating" INTEGER,
  "risk_grade" TEXT,
  "anomaly_flag" INTEGER
);
CREATE TABLE IF NOT EXISTS "nav_history" (
"Date" TIMESTAMP,
  "Nav" REAL,
  "Amfi Code" INTEGER
);
CREATE TABLE IF NOT EXISTS "investor_transactions" (
"investor_id" TEXT,
  "transaction_date" TEXT,
  "amfi_code" INTEGER,
  "transaction_type" TEXT,
  "amount_inr" INTEGER,
  "state" TEXT,
  "city" TEXT,
  "city_tier" TEXT,
  "age_group" TEXT,
  "gender" TEXT,
  "annual_income_lakh" REAL,
  "payment_mode" TEXT,
  "kyc_status" TEXT
);
CREATE TABLE IF NOT EXISTS "monthly_sip_inflows" (
"month" TEXT,
  "sip_inflow_crore" INTEGER,
  "active_sip_accounts_crore" REAL,
  "new_sip_accounts_lakh" REAL,
  "sip_aum_lakh_crore" REAL,
  "yoy_growth_pct" REAL
);
CREATE TABLE IF NOT EXISTS "calculated_performance_metrics" (
"Amfi Code" INTEGER,
  "CAGR_Annualized" REAL,
  "Annualized_Vol" REAL,
  "Sharpe_Ratio" REAL,
  "Historical_VaR_95" REAL
);
CREATE TABLE IF NOT EXISTS "recommended_funds" (
"Amfi_Code" REAL,
  "Scheme_Name" TEXT,
  "Category" TEXT,
  "Sharpe_Ratio" REAL,
  "CAGR" REAL,
  "Score" REAL
);
