FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY . /app

# Cloud providers inject PORT environment variable (default 8080 or 8888)
ENV PORT=8080
EXPOSE 8080

CMD ["python3", "server.py"]
