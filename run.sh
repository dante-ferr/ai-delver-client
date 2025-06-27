#!/bin/bash

set -e
set -o pipefail

echo "📦 Starting AI module using Docker Compose..."
cd intelligence

docker compose up -d

cd ..

echo "🖥️ Running AI Delver's $1 application..."
if [ "$1" == "game" ]; then
    poetry run python src/direct_game.py
elif [ "$1" == "ai" ]; then
    poetry run python src/direct_ai.py
else
    poetry run python src/main.py
fi

echo "🧹 Stopping AI module container..."
cd intelligence
docker compose down
