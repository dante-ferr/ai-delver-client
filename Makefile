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

# prepare-intelligence:
# 	rm -rf intelligence/runtime
# 	cp -r runtime intelligence/

on_run: update-submodules ensure-env

run-ai: on_run #prepare-intelligence
	docker compose up

run-main: on_run
	./run.sh $(ENTRYPOINT)

run: on_run prepare-intelligence
	docker compose up -d
	./run.sh $(ENTRYPOINT)