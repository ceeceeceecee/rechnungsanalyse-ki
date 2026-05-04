#!/bin/bash
set -e
echo "=== Installing rechnungsanalyse-ki ==="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is required. Please install Docker first."
    exit 1
fi
if ! docker compose version &> /dev/null; then
    echo "Docker Compose V2 is required."
    exit 1
fi

# Pull and start Ollama
echo "Starting Ollama service..."
docker compose up -d ollama
sleep 5

# Pull model
echo "Pulling llama3.1 model (this may take a while on first run)..."
docker compose exec ollama ollama pull llama3.1 2>/dev/null || echo "Model pull initiated"

# Start everything
echo "Starting all services..."
docker compose up -d

echo "=== rechnungsanalyse-ki is running ==="
echo "Open http://localhost:8501 in your browser"
