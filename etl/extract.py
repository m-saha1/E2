import requests
import time

# Endpoint for Price Paid Data (PPI)
BASE_URL = "https://landregistry.data.gov.uk/data/ppi/transaction-record.json"


def extract_data(start_year=2002, end_year=2024, samples_per_year=10):
    """
    Fetches a sample of transaction records across a range of years.
    Note: The Linked Data API performs exact matches on transactionDate.
    """
    aggregated_results = []

    print(f"[INFO] Initializing extraction for period: {start_year}-{end_year}")

    for year in range(start_year, end_year + 1):
        # We target the first of the year for consistent sampling across the range
        target_date = f"{year}-01-01"

        params = {
            "transactionDate": target_date,
            "_pageSize": samples_per_year
        }

        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(BASE_URL, params=params, headers=headers, timeout=15)

            # Check for HTTP errors
            response.raise_for_status()

            payload = response.json()
            items = payload.get("result", {}).get("items", [])

            if items:
                aggregated_results.extend(items)
                print(f"[SUCCESS] Retrieved {len(items)} records for {target_date}")
            else:
                print(f"[NOTICE] No records found for {target_date}")

            # Rate limiting to avoid 429 errors
            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to fetch data for {year}: {e}")
            continue  # Proceed to next year in the sequence

    print(f"[COMPLETED] Total records extracted: {len(aggregated_results)}")
    return aggregated_results


if __name__ == "__main__":
    # Execution entry point
    data_sample = extract_data(2002, 2024)

# Simple test run
# results = extract_data(2020, 2024)

