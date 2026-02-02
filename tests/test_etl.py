import pytest
from etl.transform import transform_and_validate


def test_extract_returns_list():
    # Verifies that the API connection is alive and returning records
    from etl.extract import extract_data
    data = extract_data()
    assert isinstance(data, list)
    assert len(data) > 0
    print(f"\n[PASSED] Extraction verified: {len(data)} records retrieved.")


def test_transform_removes_invalid_values():
    # Tests filtering of missing fields and outliers
    raw = [
        # Should drop the missing date
        {"pricePaid": 250000, "transactionDate": None},
        # Should drop the price outlier < 1000
        {"pricePaid": 500, "transactionDate": "Wed, 01 Jan 2024"},
        # Should keep the valid data
        {
            "pricePaid": 150000,
            "transactionDate": "Wed, 01 Jan 2024",
            "propertyAddress": {"postcode": "WA1 1AA"}
        }
    ]

    clean_rows, stats = transform_and_validate(raw)

    assert len(clean_rows) == 1
    assert stats["error_price_outlier"] == 1
    assert clean_rows[0]["value"] == 150000
    print("[PASSED] Filter logic verified.")


def test_transform_casts_types():
    # Tests the datetime parsing and string-to-int conversion
    raw = [
        {
            "pricePaid": {"value": "350000.50"},
            "transactionDate": "Mon, 15 May 2023",
            "propertyAddress": {"postcode": "M1 1AG"}
        }
    ]

    clean_rows, _ = transform_and_validate(raw)

    assert len(clean_rows) == 1
    assert clean_rows[0]["year"] == 2023
    assert clean_rows[0]["value"] == 350000
    assert clean_rows[0]["geography"] == "M1"
    print("[PASSED] Type casting and postcode extraction verified.")


def test_transform_provides_stats():
    # Verifies that the transformation tracks the pipeline health
    raw = [{"pricePaid": "invalid", "transactionDate": "Wed, 01 Jan 2024"}]
    _, stats = transform_and_validate(raw)

    assert stats["error_invalid_types"] >= 1
    print(f"[PASSED] Pipeline stats: {stats}")