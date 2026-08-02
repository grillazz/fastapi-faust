.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:	## Build project with compose
	docker compose build

.PHONY: up
up:	## Run project with compose
	docker compose up --remove-orphans

.PHONY: clean
clean: ## Clean Reset project containers and volumes with compose
	docker compose down -v --remove-orphans | true
	docker compose rm -f | true

.PHONY: build-apache
build-apache: ## Build project with Apache Kafka KRaft compose
	docker compose -f compose-apache-kafka.yml build

.PHONY: up-apache
up-apache: ## Run project with Apache Kafka KRaft compose
	docker compose -f compose-apache-kafka.yml up --remove-orphans

.PHONY: clean-apache
clean-apache: ## Clean Reset project containers and volumes with Apache Kafka KRaft compose
	docker compose -f compose-apache-kafka.yml down -v --remove-orphans | true
	docker compose -f compose-apache-kafka.yml rm -f | true
