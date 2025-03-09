from core.config.env import env

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://guest:guest@universitly_rabbitmq:5672//')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SOFT_TIME_LIMIT = 20
CELERY_TASK_TIME_LIMIT = 30
CELERY_TASK_MAX_RETRIES = 3
