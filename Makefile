ENTRYPOINT ?= main

.PHONY: run build ensure-env update-submodules

update-submodules:
	echo "🔁 Initializing submodules without overwriting changes..."
	git submodule update --init --recursive --merge

ensure-env:
	@if [ ! -f intelligence/.env ]; then \
	  echo "UID=$$(id -u)" > intelligence/.env; \
	  echo "GID=$$(id -g)" >> intelligence/.env; \
	  echo "📄 Created .env with UID and GID."; \
	else \
	  echo "✅ .env already exists."; \
	fi

build: update-submodules ensure-env
	docker compose build

on_run: update-submodules ensure-env

run-ai: on_run
	docker compose up

run: on_run
	./run.sh $(ENTRYPOINT)