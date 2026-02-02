from datetime import datetime

# Constants
START_YEAR = 2002
END_YEAR = 2026
DATASET_ID = "land-registry-ppi"


def transform_and_validate(items):
    clean_rows = []
    stats = {
        "raw_count": 0,
        "valid_count": 0,
        "error_missing_fields": 0,
        "error_invalid_types": 0,
        "error_out_of_bounds_year": 0,
        "error_price_outlier": 0
    }

    for item in items:
        stats["raw_count"] += 1

        # The API returns dictionaries the for price and date.
        def resolve_node(node):
            if isinstance(node, dict):
                return node.get("value") or node.get("@value")
            return node

        raw_price = resolve_node(item.get("pricePaid"))
        raw_date = resolve_node(item.get("transactionDate"))

        # Accesses the nested propertyAddress for the postcode
        address_obj = item.get("propertyAddress", {})
        raw_postcode = resolve_node(address_obj.get("postcode"))

        # Null Check for required features
        if raw_price is None or raw_date is None:
            stats["error_missing_fields"] += 1
            continue

        # Type Conversion & Temporal Validation
        try:
            # Parses the date string to extract the year correctly
            dt_obj = datetime.strptime(str(raw_date), "%a, %d %b %Y")
            obs_year = dt_obj.year

            # Uses float first to handle strings with decimals, then convert them into integers
            price_value = int(float(raw_price))

            if not (START_YEAR <= obs_year <= END_YEAR):
                stats["error_out_of_bounds_year"] += 1
                continue

            # Outlier Detection
            # Filters out non-market transfers (less than £1000) and extreme values (more than £50m)
            if price_value < 1000 or price_value > 50_000_000:
                stats["error_price_outlier"] += 1
                continue

        except (ValueError, TypeError):
            stats["error_invalid_types"] += 1
            continue

        # Extracts the Outcode
        geo_area = "UNKNOWN"
        if raw_postcode and isinstance(raw_postcode, str):
            geo_area = raw_postcode.strip().split(" ")[0].upper()

        # Appends schema-aligned dictionary
        clean_rows.append({
            "dataset_id": DATASET_ID,
            "geography": geo_area,
            "year": obs_year,
            "value": price_value
        })
        stats["valid_count"] += 1

    return clean_rows, stats
