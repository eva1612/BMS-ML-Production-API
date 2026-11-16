
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy API and trained ML model
COPY api.py .
COPY linear_regression_model.joblib .

# Expose FastAPI port
EXPOSE 8000

# Run as a non-root user
RUN useradd -m appuser
USER appuser

# Start FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
