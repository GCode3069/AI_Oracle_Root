.PHONY: help build up down logs shell test lint format clean deploy-local deploy-staging backup

help:
@echo "SCARIFY Development Commands"
@echo "=========================="
@echo "build          Build Docker images"
@echo "up             Start all services"
@echo "down           Stop all services"
@echo "logs           Show service logs"
@echo "shell          Open shell in main container"
@echo "test           Run test suite"
@echo "lint           Run code linting"
@echo "format         Format code"
@echo "clean          Clean up containers and volumes"
@echo "deploy-local   Deploy to local environment"
@echo "deploy-staging Deploy to staging environment"
@echo "backup         Create data backup"

build:
docker-compose build

up:
docker-compose up -d

down:
docker-compose down

logs:
docker-compose logs -f

shell:
docker-compose exec scarify-core bash

test:
docker-compose exec scarify-core python -m pytest tests/ -v

lint:
docker-compose exec scarify-core flake8 .
docker-compose exec scarify-core pylint scarify/

format:
docker-compose exec scarify-core black .
docker-compose exec scarify-core isort .

clean:
docker-compose down -v
docker system prune -f

deploy-local:
./scripts/deploy.ps1 -Environment local

deploy-staging:
./scripts/deploy.ps1 -Environment staging -BackupFirst

backup:
./scripts/backup.sh
