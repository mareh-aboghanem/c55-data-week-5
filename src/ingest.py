import logging
from pathlib import Path
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv()

FILES = ["messy_sales.csv", "messy_customers.csv"]
def download_inputs(data_dir: Path) -> None:
    account_url = os.getenv("ACCOUNT_URL")
    source_container = os.getenv("SOURCE_CONTAINER")
    if not account_url or not source_container:
        raise RuntimeError(
            "Please set ACCOUNT_URL and SOURCE_CONTAINER environment variables before running."
        )
    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=account_url, credential=credential)
    container = service.get_container_client(source_container)
    if not container.exists():
        logging.info(f"Container '{source_container}' not found.")
        return  
    data_dir.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        blob = container.get_blob_client(name)
        with open(data_dir / name, "wb") as f:
            f.write(blob.download_blob().readall())
        logging.info("Downloaded %s", name)


"""def load_inputs_local(data_dir: Path) -> None:
    #Because of the Fallback i implented this function to load data locally
    data_dir.mkdir(exist_ok=True)
    sample_data_dir = Path(__file__).resolve().parent.parent / "sample_data"

    for name in FILES:
        source_file = sample_data_dir / name
        destination_file = data_dir / name
        if source_file.exists():
            shutil.copy(source_file, destination_file)
            logging.info("Successfully loaded %s from local sample_data", name)
        else:
            logging.error("File %s not found in sample_data!", name)"""


def upload_outputs(output_dir: Path, github_username: str) -> None:
    """Task 7 (extra credit): Upload Parquet outputs to Azure and verify the round-trip."""
    #container_name = f"week4-{github_username}"

    # EXTRA CREDIT — implement this after Tasks 2–6 are working.
    # TODO: Create a BlobServiceClient using DefaultAzureCredential and ACCOUNT_URL.
    # TODO: Get (or create) the container named container_name.
    # TODO: Upload every .parquet file in output_dir to the container.
    # TODO: Download customer_summary.parquet back and assert its row count matches the local file.
    # TODO: Log the container name and number of files uploaded.
    pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    LOCAL_DATA_DIR = Path(__file__).resolve().parent / "data"
    download_inputs(LOCAL_DATA_DIR)
