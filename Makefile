DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app.yaml
ENV_FILE = .env
DB_CONTAINER = universitly_db
APP_CONTAINER = universitly
MANAGE = python manage.py

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} --env-file ${ENV_FILE} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} --env-file ${ENV_FILE} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE} migrate

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE} makemigrations

.PHONY: createsuperuser
createsuperuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE} collectstatic
