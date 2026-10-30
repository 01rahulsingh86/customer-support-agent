
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY agent.py main.py ./

# Run as a non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Start the API server
CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
