# Image name
IMAGE_NAME = anonymous-mailer
CONTAINER_NAME = anonymous-mailer-container
PORT = 8000

.PHONY: build run dev stop clean logs test lint format

# Build the container image using podman
build:
	podman build -t $(IMAGE_NAME) .

# Run the container
run:
	podman run -d --name $(CONTAINER_NAME) -p $(PORT):8000 --env-file .env $(IMAGE_NAME)
	@echo "Application is running at http://localhost:$(PORT)"

# Run the container in development mode (with hot-reload)
dev:
	podman run -d --name $(CONTAINER_NAME) -p $(PORT):8000 --env-file .env -v $(PWD):/app $(IMAGE_NAME)
	@echo "Application is running in DEV mode at http://localhost:$(PORT)"

# Stop and remove the container
stop:
	podman stop $(CONTAINER_NAME)
	podman rm $(CONTAINER_NAME)

# Remove the image
clean:
	podman rmi $(IMAGE_NAME)

# View logs
logs:
	podman logs -f $(CONTAINER_NAME)

# Run tests inside the container
test:
	podman run --rm --env PYTHONPATH=/app $(IMAGE_NAME) pytest

# Run linters (ruff and mypy)
lint:
	podman run --rm --env PYTHONPATH=/app $(IMAGE_NAME) ruff check .
	podman run --rm --env PYTHONPATH=/app $(IMAGE_NAME) mypy app

# Format code using ruff
format:
	podman run --rm -v $(PWD):/app $(IMAGE_NAME) ruff format .