DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
INFRA_FILE = docker_compose/infra.yaml
APP_FILE = docker_compose/app.yaml
ENV_FILE = .env
DB_CONTAINER = universitly_db
APP_CONTAINER = universitly
CELERY_CONTAINER = universitly_celery_worker
CELERY_BEAT_CONTAINER = universitly_celery_beat
MANAGE = python manage.py

.PHONY: infra
storages:
	${DC} -f ${INFRA_FILE} --env-file ${ENV_FILE} up -d

.PHONY: infra-down
storages-down:
	${DC} -f ${INFRA_FILE} down

.PHONY: infra-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${INFRA_FILE} --env-file ${ENV_FILE} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${INFRA_FILE} down

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

.PHONY: shell
shell:
	${EXEC} ${APP_CONTAINER} ${MANAGE} shell

.PHONY: celery-logs
celery-logs:
	${LOGS} ${CELERY_CONTAINER} -f

.PHONY: celery-beat-logs
celery-beat-logs:
	${LOGS} ${CELERY_BEAT_CONTAINER} -f

.PHONY: redis-logs
redis-logs:
	${LOGS} universitly_redis -f

.PHONY: rabbitmq-logs
rabbitmq-logs:
	${LOGS} universitly_rabbitmq -f
