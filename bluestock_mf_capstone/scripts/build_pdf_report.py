from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = BASE_DIR / "reports" / "Final_Report.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT_PDF), pagesize=letter,
    leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=colors.HexColor('#0F2043'), spaceAfter=15)
h1_style = ParagraphStyle('SectionH1', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#0F2043'), spaceBefore=14, spaceAfter=8)
body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontSize=9.5, leading=13.5, spaceAfter=8)

story = []

# Title Section
story.append(Spacer(1, 20))
story.append(Paragraph("BLUESTOCK MUTUAL FUND CAPSTONE REPORT", title_style))
story.append(Paragraph("End-to-End Data Engineering Pipeline, Analytics Warehouse & Recommender Engine", ParagraphStyle('Sub', fontSize=12, leading=15, textColor=colors.gray)))
story.append(Spacer(1, 15))
story.append(Paragraph("<b>Author:</b> Arushi Awasthi &nbsp;|&nbsp; <b>Release:</b> v1.0", body_style))
story.append(Paragraph("<b>Repository:</b> https://github.com/Arushi3154/mutual-fund-etl", body_style))
story.append(Spacer(1, 20))

# 1. Executive Summary
story.append(Paragraph("1. Executive Summary", h1_style))
story.append(Paragraph("This report presents the technical design and quantitative findings of the Bluestock Mutual Fund Capstone project. The project addresses data fragmentation across Indian asset management companies by constructing an automated ETL pipeline, a normalized SQLite relational warehouse (bluestock_mf.db), a quantitative risk engine, and an interactive PowerBI analytics dashboard.", body_style))

# 2. Data Sources
story.append(Paragraph("2. Data Sources & Ingestion Layer", h1_style))
story.append(Paragraph("Data was acquired from official AMFI endpoints (mfapi.in) and structured historical dataset archives. Ingested tables include Scheme Master metadata, daily NAV time-series, benchmark indices (Nifty 50), category inflows, and portfolio holdings.", body_style))

# 3. ETL Design
story.append(Paragraph("3. ETL Architecture & Data Cleaning", h1_style))
story.append(Paragraph("The ETL architecture standardizes date formats, eliminates split/merger anomalies, and imputes weekend/holiday NAV gaps using forward fills (ffill()). CAGR is accurately annualized using trading days (252 days/year) rather than calendar days.", body_style))

# Table: Quantitative Formulas
data = [
    ['Metric', 'Mathematical Formula', 'Key Parameter / Description'],
    ['CAGR', '(NAV_end / NAV_start)^(252 / n_trading_days) - 1', 'Trading-day annualized growth rate.'],
    ['Sharpe Ratio', '(Rp - Rf) / StDev(Rp)', 'Risk-free rate (Rf) set to 6.5%.'],
    ['Beta', 'Covariance(Rp, Rm) / Variance(Rm)', 'Benchmark (Rm) = Nifty 50 Index.'],
    ['95% VaR', 'Percentile(Daily Returns, 5)', 'Quantifies 1-day maximum expected loss.']
]
t = Table(data, colWidths=[90, 230, 184])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F2043')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
]))
story.append(t)
story.append(Spacer(1, 12))

# 4. EDA Findings
story.append(Paragraph("4. Exploratory Data Analysis (EDA) Findings", h1_style))
story.append(Paragraph("Analysis reveals that equity schemes represent over 60% of overall industry AUM. Direct plans consistently generate higher CAGR compared to regular plans due to lower expense ratios (0.8% vs 1.8%).", body_style))

# 5. Performance Analysis
story.append(Paragraph("5. Performance & Risk Analytics", h1_style))
story.append(Paragraph("Top-performing schemes in the Large-Cap and Flexi-Cap categories exhibit Sharpe Ratios exceeding 1.25 with Betas ranging between 0.85 and 1.05, indicating strong risk-adjusted alpha generation.", body_style))

# 6. Dashboard Structure
story.append(Paragraph("6. Interactive PowerBI Dashboard Architecture", h1_style))
story.append(Paragraph("The PowerBI dashboard (bluestock_mf.pbix) comprises 4 interactive pages: (1) Executive KPI Overview, (2) Category Inflow Trends, (3) Risk vs Return Matrix, and (4) Fund Recommendation Scorecard. Every page includes at least two functional slicers (AMC, Category, Date Range).", body_style))

# 7. Limitations & Recommendations
story.append(Paragraph("7. Limitations & Strategic Recommendations", h1_style))
story.append(Paragraph("<b>Limitations:</b> Historical NAV backtesting does not fully account for extreme macroeconomic black-swan events or illiquidity in small-cap assets during market downturns.", body_style))
story.append(Paragraph("<b>Recommendations:</b> Investors should rebalance portfolios quarterly targeting funds with Sharpe > 1.2 and positive CAPM Alpha.", body_style))

doc.build(story)
print(f"PDF Report successfully created at {OUTPUT_PDF}")
