.PHONY: all

build:
	docker-compose build

start:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down --rmi local

test:
	docker-compose -f docker-compose.testing.yml -p testing build
	docker-compose -f docker-compose.testing.yml -p testing up --exit-code-from tests
	docker-compose -f docker-compose.testing.yml -p testing down --rmi local

publish:
	@echo ${DOCKER_HUB_PASSWORD} > docker login --username=${DOCKER_HUB_USER} --password-stdin
	docker build . -t ${DOCKER_HUB_USER}/rest-server
	docker push ${DOCKER_HUB_USER}/rest-server
