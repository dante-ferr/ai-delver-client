#!/bin/bash

set -e
set -o pipefail

echo "📦 Starting AI module using Docker Compose..."

execute_intelligence_container() {
    cd intelligence
    docker compose up -d
    cd ..
}

echo "🖥️ Running AI Delver's $1 application..."
if [ "$1" == "game" ]; then
    poetry run python src/direct_game.py
elif [ "$1" == "ai" ]; then
    execute_intelligence_container
    poetry run python src/direct_ai.py
elif [ "$1" == "editor" ]; then
    poetry run python src/main.py
else
    execute_intelligence_container
    poetry run python src/main.py
fi

echo "🧹 Stopping AI module container..."
cd intelligence
docker compose down
