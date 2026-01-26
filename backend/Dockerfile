# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend code (core folder)
COPY core ./core

# Expose port for FastAPI
EXPOSE 8000

# Run the app
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
