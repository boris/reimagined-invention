include .env_vars
export $(shell sed 's/=.*//' .env_vars)

.PHONY: build db-init db-load db-migrate db-up db-upgrade help run run-db tunnel

.DEFAULT_GOAL := help

TAG := $(shell git describe --tags --abbrev=0)
IMAGE := "111285186890.dkr.ecr.us-east-1.amazonaws.com/reimagined-invention"
GIT_COMMIT_HASH := $(shell git rev-parse --short HEAD)
export GIT_COMMIT_HASH

build: ## Build the docker image
	docker build -t $(IMAGE):$(GIT_COMMIT_HASH) .
	docker tag $(IMAGE):$(GIT_COMMIT_HASH) $(IMAGE):$(TAG)

push: ## Push the docker image to ECR
	#aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 111285186890.dkr.ecr.us-east-1.amazonaws.com
	docker push $(IMAGE):$(GIT_COMMIT_HASH)
	docker push $(IMAGE):$(TAG)

db-init: ## Init the DB for SQLAlchemy
	flask --app app --debug db init

db-help: ## Shows help for DB commands
	@echo "Run DB commads in the following order:"
	@echo
	@echo "db-up (if needed)"
	@echo "db-init (if needed)"
	@echo "db-migrate"
	@echo "db-upgrade"
	@echo "db-load (if needed)"
	@echo
	@echo "See help <db-command> for help."

db-load: ## Dumps a sample dataset into the DB
	mysql -h 127.0.0.1 -u root -p reimagined_invention < reimagined_invention.sql

db-migrate: ## Creates a migration file for the DB schema
	flask --app app --debug db migrate

db-up: ## Starts the DB engine using docker
	docker run -d -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=supersecret -d mysql:5.7

db-upgrade: ## Applies the migration plan
	flask --app app --debug db upgrade

help: ## Show this help
	@echo "If in doubt, start with make run"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

run-docker: ## Run the Flask app in docker using latest build
	docker run -p 5000:5000 $(IMAGE):$(GIT_COMMIT_HASH)

run: ## Run the Flask app in local (debug) mode
	flask --app app --debug run --host=0.0.0.0

run-db: ## Start the DB service in docker
	docker run -d -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) -d mysql:5.7

tunnel: ## Exposes the local environment on test.lenore.me. This will run `make run` in the background first.
	$(MAKE) run &
	docker run cloudflare/cloudflared:latest tunnel --no-autoupdate --metrics 0.0.0.0:60123 run --token $(CF_TOKEN)
