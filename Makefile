default: help

.PHONY: db-migrate db-upgrade help run

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
	flask --app app --debug run

