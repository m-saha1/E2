from etl.extract import extract_data
from etl.transform import transform_and_validate
from etl.load import load_data
import logging

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("etl.log"),  # Saves to etl.log file
        logging.StreamHandler()  # Also prints to terminal
    ]
)
logger = logging.getLogger(__name__)


def run_etl():
    logger.info("\n[ETL Pipeline Process Started]\n")

    # Extraction phase
    raw_items = extract_data()

    # Transformation phase with validation logic
    clean_rows, stats = transform_and_validate(raw_items)

    logger.info("\n[--- ETL Transformation Stats ---]\n")
    for k, v in stats.items():
        logger.info(f"{k}: {v}")

    # Loading
    load_data(clean_rows)
    logger.info("\n[ETL Pipeline Process Complete - Data loaded to PostgreSQL]\n")


if __name__ == "__main__":
    run_etl()

