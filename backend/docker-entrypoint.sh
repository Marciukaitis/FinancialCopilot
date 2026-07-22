#!/bin/sh
set -e

OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://ollama:11434}"

echo "Waiting for Ollama at ${OLLAMA_BASE_URL}..."
until curl -sf "${OLLAMA_BASE_URL}/api/tags" >/dev/null 2>&1; do
  sleep 2
done
echo "Ollama is reachable."

mkdir -p /app/data/chroma /app/data/documents

exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
