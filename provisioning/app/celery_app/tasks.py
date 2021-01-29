import time

from celery_app.worker import celery_app


@celery_app.task
def provision(**kwargs):
    time.sleep(60)
    print("inside task")
