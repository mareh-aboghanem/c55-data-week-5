"""
Week 5 assignment: containerised data pipeline.

Tasks:
- Task 1: confirm this script runs locally before touching the Dockerfile.
- Task 5: read all configuration from environment variables (no hardcoded values).

Replace every `raise NotImplementedError` below with a real implementation.
"""
# python -m src.pipeline
import os
import logging
from pathlib import Path
from src.ingest import download_inputs, upload_outputs
from src.clean import load_and_explore, clean_sales
from src.transform import join_customers
from src.report import build_reports, write_outputs

GITHUB_USERNAME = "mareh-aboghanem"
DATA_DIR = Path("data")
# OUTPUT_DIR = Path("output")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_config() -> dict:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY environment is required but its value is missing.")
    
    output_dirctroy = os.getenv("OUTPUT_DIR", "output")

    return {"api_key": api_key, "output_dir": output_dirctroy}


def fetch_data(api_key: str) -> list[dict]:
    """
    Simulate fetching records from an external API.

    Return a list of at least one dict representing a record.
    In a real pipeline you would call requests.get(...) here.
    """
    mock_record = {
        "transaction_id": 999,
        "product_name": "Mock Test Item",
        "category": "Testing",
        "price": 99.99,
        "quantity": 1,
        "customer_email": "test_user@example.com",
        "date": "2026-06-03",
    }
    return [mock_record]


def save_results(records: list[dict], output_dir: Path) -> None:
    """
    Write each record as a line to output_dir/results.txt.

    Create output_dir if it does not exist.
    Log the number of records written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "results.txt", "w") as f:
        for record in records:
            f.write(f"{record}\n")
    logging.info("Saved %d records to %s", len(records), output_dir / "results.txt")

# 5
def run() -> None:
    config = get_config()
    logger.info("starting pipeline")
    records = fetch_data(config["api_key"])
    output_dir = Path(config["output_dir"])
    save_results(records, output_dir)
    download_inputs(DATA_DIR)
    sales_raw, customers_raw = load_and_explore(DATA_DIR)
    sales_clean = clean_sales(sales_raw)
    enriched = join_customers(sales_clean, customers_raw)
    reports = build_reports(enriched)
    write_outputs(reports, output_dir)
    # upload_outputs(OUTPUT_DIR, GITHUB_USERNAME)
    logging.info("Pipeline complete.")


if __name__ == "__main__":
    run()
