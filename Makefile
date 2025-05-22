ENTRYPOINT ?= main

.PHONY: run build ensure-env update-submodules

update-submodules:
	echo "🔁 Initializing submodules without overwriting changes..."
	git submodule update --init --recursive --merge

ensure-env:
	@if [ ! -f ai_delver_intelligence/.env ]; then \
	  echo "UID=$$(id -u)" > ai_delver_intelligence/.env; \
	  echo "GID=$$(id -g)" >> ai_delver_intelligence/.env; \
	  echo "📄 Created .env with UID and GID."; \
	else \
	  echo "✅ .env already exists."; \
	fi

build: update-submodules ensure-env
	cd ai_delver_intelligence && docker compose build

on_run: update-submodules ensure-env

run-ai: on_run
	cd ai_delver_intelligence && docker compose up

run-main: on_run
	./run.sh $(ENTRYPOINT)

run: on_run
	cd ai_delver_intelligence && docker compose up -d
	./run.sh $(ENTRYPOINT)