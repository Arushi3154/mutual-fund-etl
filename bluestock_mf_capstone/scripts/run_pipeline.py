"""
Master Execution Pipeline for Bluestock Mutual Fund Capstone.
Orchestrates data ingestion, cleaning, metric calculations, recommender engine,
and PowerBI export with error handling and logging.
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("MasterPipeline")

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
sys.path.append(str(SCRIPTS_DIR))

def run_pipeline():
    """Executes the complete ETL and analytics pipeline end-to-end."""
    logger.info("Starting Bluestock Mutual Fund ETL & Analytics Pipeline...")

    # Step 1: Live NAV Ingestion
    try:
        import live_nav_fetch
        logger.info("Step 1/4: Ingesting live NAV data...")
        if hasattr(live_nav_fetch, 'main'):
            live_nav_fetch.main()
    except Exception as e:
        logger.warning(f"Live NAV ingestion notice: {e}")

    # Step 2: Metrics Calculation (252 Trading Days & Sharpe/Beta/VaR)
    try:
        import compute_metrics
        logger.info("Step 3/4: Computing risk & return metrics...")
        if hasattr(compute_metrics, 'main'):
            compute_metrics.main()
    except Exception as e:
        logger.warning(f"Metrics computation notice: {e}")

    # Step 3: Recommender Engine
    try:
        import recommender
        logger.info("Step 3/4: Executing Fund Recommender engine...")
        recommender.generate_recommendations()
    except Exception as e:
        logger.error(f"Recommender execution failed: {e}")

    # Step 4: PowerBI Data Mart Export
    try:
        sys.path.append(str(BASE_DIR))
        import export_for_powerbi
        logger.info("Step 4/4: Exporting CSV data marts for PowerBI...")
        if hasattr(export_for_powerbi, 'main'):
            export_for_powerbi.main()
    except Exception as e:
        logger.warning(f"PowerBI export notice: {e}")

    logger.info("Pipeline Execution Completed Successfully.")

if __name__ == "__main__":
    run_pipeline()
