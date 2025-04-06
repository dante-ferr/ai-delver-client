.PHONY: run build ensure-env

ensure-env:
	@if [ ! -f ai_delver_intelligence/.env ]; then \
	  echo "UID=$$(id -u)" > ai_delver_intelligence/.env; \
	  echo "GID=$$(id -g)" >> ai_delver_intelligence/.env; \
	  echo "📄 Created .env with UID and GID."; \
	else \
	  echo "✅ .env already exists."; \
	fi

run: ensure-env
	./run.sh

build: ensure-env
	cd ai_delver_intelligence && docker compose up --build -d