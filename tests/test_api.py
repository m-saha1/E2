from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_health():
    # Verifies the API data root is responsive
    response = client.get("/data/")
    assert response.status_code == 200
    print("\n[PASSED] API Health Check successful.")

def test_get_housing_data():
    # Tests the primary data retrieval endpoint
    response = client.get("/data/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print(f"[PASSED] Housing data retrieved: {len(response.json())} records found.")

def test_housing_response_structure():
    # Makes sure that the output matches the model
    response = client.get("/data/")
    data = response.json()
    if len(data) > 0:
        item = data[0]
        assert "geography" in item
        assert "year" in item
        assert "value" in item
        print(f"[PASSED] Record structure validated.")

def test_average_value_analytics():
    # Tests the analytical aggregation endpoint
    response = client.get("/analytics/average-price")
    assert response.status_code == 200
    print(f"[PASSED] Analytics result: {response.json()}")