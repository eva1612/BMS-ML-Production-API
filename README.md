# BMS ML Production API

## 1. Project Overview

A Machine Learning based REST API that predicts battery cell voltage using battery parameters. It uses a trained Linear Regression model with FastAPI and Docker for deployment.

## 2. Technologies Used

- Python
- FastAPI
- Scikit-learn
- Joblib
- Pydantic
- Pytest
- Docker
- Uvicorn

## 3. Project Structure

```text
BMS-ML-Production-API/
 api.py
linear_regression_model.joblib
test_api.py
requirements.txt
Dockerfile
.dockerignore
.gitignore
README.md
```

## 4. API Endpoints

| Method | Endpoint | Purpose |
| GET    | `/`      | Check API status |
| POST   | `/predict` | Predict battery cell voltage |

Example prediction response:

```json
{
  "temperature": 25,
  "soc": 80,
  "predicted_cell_voltage": 3.9312
}
```

## 5. Input Validation

Pydantic validates the input parameters, including temperature, current, power, converter command, SOC and SOH. Invalid or missing values return a 422 error.

## 6. Run Locally

```bash
git clone https://github.com/eva1612/BMS-ML-Production-API.git
cd BMS-ML-Production-API
pip install -r requirements.txt
uvicorn api:app --reload
```

Open `http://localhost:8000/docs` to access Swagger UI.

## 7. Unit Testing

Run tests using:

```bash
pytest -v
```

**Result: 8 tests passed.**

Tests cover valid inputs, invalid inputs, missing fields and boundary values.

## 8. Docker Deployment

Build the image:

```bash
docker build -t bms-ml-api .
```

Run the container:

```bash
docker run -d -p 8001:8000 --name bms-container bms-ml-api
```

Access the API at `http://localhost:8001/docs`.

