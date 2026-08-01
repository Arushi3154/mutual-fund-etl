# Mutual Fund ETL Project
<div align="center">

# 📈 Mutual Fund Data Analytics & ETL Engine
### *Bluestock Mutual Fund Analytics Capstone*

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Database](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Data Stack](https://img.shields.io/badge/Pandas-Seaborn-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Build Status](https://img.shields.io/badge/Pipeline-Passing-brightgreen?style=for-the-badge)

---

**An end-to-end automated ETL pipeline and analytical processing engine built to analyze market trends, investor demographics, AUM growth, and portfolio concentration across Indian Mutual Funds (2022–2026).**

[Executive Summary](#-executive-dashboard-summary) • [Architecture](#%EF%B8%8F-etl-pipeline-architecture) • [Analytics Highlights](#-key-analytics--visual-dashboards) • [Quick Start](#-getting-started) • [Repo Structure](#-repository-structure)

---

</div>

## 📊 Executive Dashboard Summary

| Metric | Status / Value | Description |
| :--- | :--- | :--- |
| **Pipeline Status** | `COMPLETED (Day 3)` | End-to-end data processing and automated notebook generation active |
| **Primary Storage** | `bluestock_mf.db` | Embedded SQLite relational database store |
| **Historical Range** | `2022 – 2026` | Multi-year NAV trends, SIP inflow streams, and portfolio snapshots |
| **Peak SIP Inflow** | `₹31,002 Cr` | Benchmark retail monthly SIP volume recorded in pipeline output |
| **AUM Benchmark** | `₹12.5 Lakh Cr` | Peak AMC Assets Under Management tracked (SBI Mutual Fund) |
| **Visual Assets** | `15+ Generated` | Automated Seaborn & Plotly chart creation into `/reports/figures/` |

---

## 🏗️ ETL Pipeline Architecture
                               [ RAW DATA SOURCE ]
                                       │
                                       ▼
                        ┌─────────────────────────────┐
                        │  Extraction & Normalization │
                        │ (Handling Schemas & Types)  │
                        └──────────────┬──────────────┘
                                       │
                                       ▼
                        ┌─────────────────────────────┐
                        │  Relational Database Layer  │
                        │      (bluestock_mf.db)      │
                        └──────────────┬──────────────┘
                                       │
                                       ▼
                        ┌─────────────────────────────┐
                        │   EDA & Analytics Pipeline  │
                        │        (run_eda.py)         │
                        └──────────────┬──────────────┘
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           ▼                                                       ▼
┌───────────────────────────────┐                       ┌───────────────────────────────┐
│   Static & Interactive Charts │                       │  Automated Jupyter Analytics  │
│     (reports/figures/*.png)   │                       │      (EDA_Analysis.ipynb)     │
└───────────────────────────────┘                       └───────────────────────────────┘


---

## 🔑 Key Analytics & Visual Dashboards

The execution engine automatically builds and exports high-resolution visual insights directly into `reports/figures/` and compiles an interactive summary notebook `EDA_Analysis.ipynb`.

### 1. 📈 NAV Historical Performance & Regime Analysis
* **Engine:** Plotly Express
* **Output:** `01_nav_trend.png`
* **Key Insight:** Tracks daily Net Asset Value trajectories across leading schemes, highlighting the **2023 Bull Run** and **2024 Market Correction** regimes.

### 2. 🏛️ AMC Market Leadership & AUM Dominance
* **Engine:** Seaborn Categorical Plots
* **Output:** `02_aum_growth.png`
* **Key Insight:** Highlights top-tier AMC expansion, showing **SBI Mutual Fund** maintaining industrial dominance crossing **₹12.5 Lakh Crore**.

### 3. 💸 Systematic Investment Plan (SIP) Dynamics
* **Engine:** Time-Series Plotly
* **Output:** `03_sip_inflows.png`
* **Key Insight:** Documents the exponential trajectory of monthly retail SIP contributions rising from **₹11,500 Cr** (Jan 2022) to an all-time peak of **₹31,002 Cr**.

### 4. 👥 Demographics & Geographical Penetration
* **Engine:** Multi-Panel Subplot Arrays
* **Output:** `05_demographics_panel.png`, `06_geographic_dist.png`
* **Key Insight:**
  * **Age Cohorts:** The 18–30 demographic holds >40% of unique folios, while the 31–50 age band drives the highest average ticket size per transaction.
  * **Geographic Shift:** **B30 (Beyond Top 30)** cities now contribute **40%** of aggregate inflows, marking a significant transition into Tier-2 & Tier-3 regional markets.

### 5. 🍩 Sector Diversification & Portfolio Correlation
* **Engine:** Correlation Heatmaps & Donut Charts
* **Output:** `08_correlation_matrix.png`, `09_sector_donut.png`
* **Key Insight:** Financial Services and Information Technology constitute over **50%** of total equity portfolio holdings, demonstrating high intra-sector NAV correlation.

---

## 📂 Repository Structure

```directory
mutual-fund-etl/
├── bluestock_mf.db          # SQLite Relational Database Engine
├── run_eda.py               # Core Analytical & Pipeline Execution Script
├── EDA_Analysis.ipynb       # Automatically Generated Business Intelligence Notebook
├── reports/
│   └── figures/             # High-Resolution Chart Renderings (.png)
│       ├── 01_nav_trend.png
│       ├── 02_aum_growth.png
│       ├── 03_sip_inflows.png
│       ├── 04_category_heatmap.png
│       ├── 05_demographics_panel.png
│       ├── 06_geographic_dist.png
│       ├── 07_folio_growth.png
│       ├── 08_correlation_matrix.png
│       └── 09_sector_donut.png
├── requirements.txt         # Project Dependencies
└── README.md                # Project Dashboard & Documentation
⚡ Getting Started
Prerequisites
Python 3.10+
Virtual environment configured
Installation & Execution
Clone the repository:
Bash
git clone [https://github.com/your-username/mutual-fund-etl.git](https://github.com/your-username/mutual-fund-etl.git)
cd mutual-fund-etl
Activate your Virtual Environment:
Bash
source venv/bin/activate   # On macOS/Linux
# or
.\venv\Scripts\activate    # On Windows
Install Dependencies:
Bash
pip install -r requirements.txt
Run the ETL & EDA Pipeline:
Bash
python3 run_eda.py
🛠️ Tech Stack & Tools
Core Language: Python 3.14
Data Processing & Manipulation: Pandas, NumPy
Relational Storage: SQLite3
Visualization Engines: Seaborn, Matplotlib, Plotly Express
Automated Notebook Generation: nbformat
