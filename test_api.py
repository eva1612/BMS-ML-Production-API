
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

# Valid input data
valid_data = {
    "temperature": 25.0,
    "module_current_a": 10.0,
    "module_power_kw": 5.0,
    "converter_command_pct": 50.0,
    "soc": 80.0,
    "soh": 95.0
}


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == \
        "BMS Cell Voltage Prediction API is running"


def test_valid_prediction():
    response = client.post("/predict", json=valid_data)

    assert response.status_code == 200
    assert "predicted_cell_voltage" in response.json()
    assert isinstance(
        response.json()["predicted_cell_voltage"], float
    )


def test_invalid_temperature():
    data = valid_data.copy()
    data["temperature"] = 150

    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_missing_fields():
    data = {
        "temperature": 25.0,
        "soc": 80.0
    }

    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_boundary_values():
    data = {
        "temperature": -50,
        "module_current_a": 0,
        "module_power_kw": 0,
        "converter_command_pct": 0,
        "soc": 0,
        "soh": 0
    }

    response = client.post("/predict", json=data)
    assert response.status_code == 200


def test_maximum_boundary_values():
    data = {
        "temperature": 100,
        "module_current_a": 100,
        "module_power_kw": 100,
        "converter_command_pct": 100,
        "soc": 100,
        "soh": 100
    }

    response = client.post("/predict", json=data)
    assert response.status_code == 200


def test_negative_current():
    data = valid_data.copy()
    data["module_current_a"] = -5

    response = client.post("/predict", json=data)
    assert response.status_code == 422


def test_invalid_soc():
    data = valid_data.copy()
    data["soc"] = 120

    response = client.post("/predict", json=data)
    assert response.status_code == 422
