from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import os

app = FastAPI()

model_path = os.path.join(
    os.path.dirname(__file__),
    "linear_regression_model.joblib"
)

model = joblib.load(model_path)


class BatteryInput(BaseModel):
    temperature: float = Field(..., ge=-50, le=100)
    module_current_a: float = Field(..., ge=0)
    module_power_kw: float = Field(..., ge=0)
    converter_command_pct: float = Field(..., ge=0, le=100)
    soc: float = Field(..., ge=0, le=100)
    soh: float = Field(..., ge=0, le=100)
class BatteryOutput(BaseModel):
    temperature: float
    soc: float
    predicted_cell_voltage: float


@app.get("/")
def home():
    return {
        "message": "BMS Cell Voltage Prediction API is running"
    }


@app.post("/predict", response_model=BatteryOutput)
def predict(data: BatteryInput):

    features = [[
        data.temperature,
        data.module_current_a,
        data.module_power_kw,
        data.converter_command_pct,
        data.soc,
        data.soh
    ]]

    prediction = model.predict(features)[0]

    return {
        "temperature": data.temperature,
        "soc": data.soc,
        "predicted_cell_voltage": round(float(prediction), 4)
    }