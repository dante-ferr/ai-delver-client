#!/bin/bash

set -e
set -o pipefail

echo "📦 Starting AI module using Docker Compose..."
cd ai_delver_intelligence

docker compose up -d

cd ..

echo "🖥️ Running AI Delver's $1 application..."
if [ "$1" == "game" ]; then
    pipenv run python3 src/direct_game.py
elif [ "$1" == "ai" ]; then
    pipenv run python3 src/direct_ai.py
else
    pipenv run python3 src/main.py
fi

echo "🧹 Stopping AI module container..."
cd ai_delver_intelligence
docker compose down
