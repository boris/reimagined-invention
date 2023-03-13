default: help

include .env_vars
export $(shell sed 's/=.*//' .env_vars)

.PHONY: db-migrate db-upgrade help run run-db tunnel

db-migrate: ## Creates a migration file for the DB schema
	flask --app app --debug db migrate

db-upgrade: ## Applies the migration plan
	flask --app app --debug db upgrade

help: ## Show this help
	@echo "If in doubt, start with make run"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

run: ## Run the Flask app in local (debug) mode
	flask --app app --debug run --host=0.0.0.0

run-db: ## Start the DB service in docker
	docker run -d -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) -d mysql:5.7

tunnel: ## Exposes the local environment on test.lenore.me. This requires a `make run` first.
	docker run cloudflare/cloudflared:latest tunnel --no-autoupdate --metrics 0.0.0.0:60123 run --token $(CF_TOKEN)
