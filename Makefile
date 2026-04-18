.PHONY: dev backend frontend install build docker-build docer-run

dev:
	@echo "Starting development environment..."
	python scripts/dev.py

backend:
	@echo "Starting Flask backend..."
	cd flaskr && FLASK_APP=app.py FLASK_ENV=development flask run

frontend:
	@echo "Starting React frontend..."
	cd frontend && npm start

install:
	@echo "Installing dependencies..."
	pip install -e .
	cd frontend && npm install

build:
	@echo "Building frontend..."
	cd frontend && npm run build

docker-build:
	@echo "Building Docker image..."
	docker build -t cains-jawbone .

docker-run:
	@echo "Running Docker container..."
	docker run -p 5000:5000 cains-jawbone