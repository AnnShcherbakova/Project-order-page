from celery import Celery

app = Celery(
   'project',  # Имя проекта
   broker='redis://localhost:6379/0',  # URL брокера Redis
   backend='redis://localhost:6379/0'  # URL бэкенда Redis
)
