SELECT f.scheme_name, a.total_aum 
FROM fact_aum a
JOIN dim_fund f ON a.amfi_code = f.amfi_code
ORDER BY a.total_aum DESC 
LIMIT 5;

SELECT f.scheme_name, d.year, d.month, AVG(n.nav) as avg_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.date_id = d.date_id
GROUP BY f.scheme_name, d.year, d.month
ORDER BY d.year DESC, d.month DESC;

SELECT d.year, SUM(t.amount) as total_sip_volume,
       LAG(SUM(t.amount)) OVER (ORDER BY d.year) as prev_year_volume,
       ((SUM(t.amount) - LAG(SUM(t.amount)) OVER (ORDER BY d.year)) / 
        LAG(SUM(t.amount)) OVER (ORDER BY d.year)) * 100 as yoy_growth_pct
FROM fact_transactions t
JOIN dim_date d ON t.date_id = d.date_id
WHERE t.transaction_type = 'SIP'
GROUP BY d.year;

SELECT i.state, COUNT(t.transaction_id) as txn_count, SUM(t.amount) as total_volume
FROM fact_transactions t
JOIN dim_investor i ON t.investor_id = i.investor_id
GROUP BY i.state
ORDER BY total_volume DESC;

SELECT f.scheme_name, f.category, p.expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;


SELECT f.category, f.scheme_name, p.3yr_return
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE (
    SELECT COUNT(*) FROM fact_performance p2 
    JOIN dim_fund f2 ON p2.amfi_code = f2.amfi_code 
    WHERE f2.category = f.category AND p2.3yr_return > p.3yr_return
) < 3 
ORDER BY f.category, p.3yr_return DESC;

SELECT transaction_type, COUNT(transaction_id) as total_transactions, SUM(amount) as total_value
FROM fact_transactions
WHERE transaction_type IN ('REDEMPTION', 'LUMPSUM')
GROUP BY transaction_type;


SELECT f.scheme_name, p.1yr_return, p.expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.anomaly_flag = 1;

SELECT f.scheme_name, MAX(n.nav) as max_nav, MIN(n.nav) as min_nav, 
       (MAX(n.nav) - MIN(n.nav)) as volatility_spread
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name
ORDER BY volatility_spread DESC
LIMIT 10;


SELECT state, 
       SUM(CASE WHEN kyc_status = 'REJECTED' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as rejection_rate_pct
FROM dim_investor
GROUP BY state
ORDER BY rejection_rate_pct DESC;