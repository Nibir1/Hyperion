# Force rebuild to ensure dependencies are fresh
build:
	docker-compose build --no-cache
	docker-compose up -d
	@echo "Application running at http://localhost:3000"

tests:
	docker-compose exec backend pytest --cov=app tests/

up:
	docker-compose up -d
	@echo "Application running at http://localhost:3000"

down:
	docker-compose down

logs:
	docker-compose logs -f

# Nuclear option: wipes database data too
clean:
	docker-compose down -v
	docker system prune -f

# Debugging helper
shell-backend:
	docker-compose exec backend /bin/bash

.PHONY: build up down logs clean shell-backend tests