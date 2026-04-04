.PHONY: dev dev-backend dev-frontend test build clean seed

# Start all services (development)
dev: dev-backend dev-frontend

dev-backend:
	py -m uvicorn backend.main:app --port 8111 --reload

dev-frontend:
	cd frontend && npx ng serve --port 4222

# Run tests
test:
	py -m pytest backend/tests/test_articles.py backend/tests/test_scoring.py backend/tests/test_student_and_judge.py -v

# Build frontend
build:
	cd frontend && npx ng build --configuration=production

# Docker
docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

# Seed sample data (upload articles + generate 3 dataset items)
seed:
	curl -s -X POST http://localhost:8111/api/articles/upload -F "file=@aljazeera_arabic_news_dataset_100_articles.json"
	curl -s -X POST "http://localhost:8111/api/dataset/generate?limit=3"

# Clean database
clean:
	rm -f backend/data/benchmark.db
	@echo "Database cleaned"
