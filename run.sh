#!/bin/bash

set -e
set -o pipefail

echo "🔁 Initializing submodules without overwriting changes..."
git submodule update --init --recursive --merge

echo "📦 Starting AI module using Docker Compose..."
cd ai_delver_intelligence

docker compose up -d

cd ..

echo "🖥️ Running AI Delver main application..."
pipenv run start

echo "🧹 Stopping AI module container..."
cd ai_delver_intelligence
docker compose down
