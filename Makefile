MODE ?= prod

SERVICES_DEV = dev_db dev pg_admin
SERVICES_PROD = prod_db prod pg_admin
SERVICES_TEST = test_db test
SERVICES = $(SERVICES_$(shell echo $(MODE) | tr 'a-z' 'A-Z'))

build:
	@echo "Building for $(MODE) mode..."
	cp .env.$(MODE) .env
	docker-compose build $(SERVICES) --no-cache

run:
	@echo "Running in $(MODE) mode..."
	cp .env.$(MODE) .env
	docker-compose up $(SERVICES)

#test:
#	@echo "Running tests in test mode..."
#	cp .env.test .env
#	docker-compose run --rm test
test:
	@echo "Running tests in test mode..."
	cp .env.test .env
	docker-compose up --abort-on-container-exit --exit-code-from test test_db test


rebuild:
	cp .env.$(MODE) .env
	docker-compose up --build --force-recreate $(SERVICES)

down:
	docker-compose down

logs:
	docker-compose logs -f