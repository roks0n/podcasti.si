NAME=podcasts
PACKAGE_NAME=podcasts


DOCKER_MACHINE_NAME := $(shell echo $${DOCKER_MACHINE_NAME:-default})
RAW_DOCKER_IP=$(shell docker-machine ip ${DOCKER_MACHINE_NAME} 2>/dev/null)
DOCKER_IP=$(if $(RAW_DOCKER_IP),$(RAW_DOCKER_IP),"127.0.0.1")

COLOR_HL := \033[33m
COLOR_RESET := \033[0m


.PHONY: dev-bootstrap
dev-bootstrap: build wakeup-database migrate collectstatic ## Initial set up of development environment

.PHONY: build
build:
	docker-compose build $(NAME)

.PHONY: runserver
runserver: ## Run podcasts service
	@echo "==="
	@echo "You can find podcasts by pointing your browser at $(COLOR_HL)$(DOCKER_IP):8000$(COLOR_RESET)"
	@echo "==="
	docker-compose up $(NAME)

.PHONY: wakeup-database
wakeup-database:
	docker-compose up -d db
	@echo "==="
	@echo "Sleeping for a few seconds to make sure the database wakes up!"
	@echo "==="
	sleep 3s

.PHONY: bash
bash: ## Start a bash shell in the container environment
	docker-compose run --rm $(NAME) bash

.PHONY: shell
shell: ## Start a Python shell in the container environment
	docker-compose run --rm $(NAME) django-admin shell

.PHONY: dbshell
dbshell: ## Start a database shell in the container environment
	docker-compose run --rm $(NAME) django-admin dbshell

.PHONY: data-shell
data-shell: ## Start a database shell in the container environment
	docker-compose run --rm $(NAME) django-admin data-shell

.PHONY: migrations
migrations: ## Generate database migration scripts
	docker-compose run --rm $(NAME) django-admin makemigrations $(PACKAGE_NAME)

.PHONY: migrate
migrate: ## Run database migration scripts
	docker-compose run --rm $(NAME) django-admin migrate

.PHONY: collectstatic
collectstatic:
	docker-compose run --rm $(NAME) django-admin collectstatic --noinput

.PHONY: superuser
superuser:
	docker-compose run --rm $(NAME) django-admin createsuperuser

.PHONY: lint-diff
lint-diff: ## Check code for quality and standards on changed files only
	git diff upstream/master src tests | flake8 --select=E,F,I,W --diff

.PHONY: clean-pyc
clean-pyc:
	find . -name "*.pyc" -type f -delete

.PHONY: docker-clean-containers
docker-clean-containers: ## Remove all docker containers
	@echo Removing all containers
	-docker ps -aq | xargs docker rm -f

.PHONY: docker-clean-images
docker-clean-images: ## Remove all docker images
	@echo Removing old images
	-docker images -q -f="dangling=true" | xargs docker rmi

.PHONY: docker-clean
docker-clean: docker-clean-containers docker-clean-images
