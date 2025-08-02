#!/bin/bash

set -e
set -o pipefail

echo "🖥️ Running AI Delver's client application on the '$1' entrypoint..."
if [ "$1" == "game" ]; then
    poetry run python src/direct_game.py
elif [ "$1" == "ai" ]; then
    poetry run python src/direct_ai.py
elif [ "$1" == "editor" ]; then
    poetry run python src/main.py
else
    poetry run python src/main.py
fi