import time

from celery_app.worker import celery_app
from core.host import Host
from config import Config


@celery_app.task
def provision(ip, task_type):
    c = Config()
    credentials = c.credentials[task_type]
    if credentials:
        host = Host(
            ip=ip,
            username=credentials["username"],
            password=credentials["password"]
        )
        print("sleeping 180 seconds")
        time.sleep(180)
        print("upgrading device")
        host.upgrade_device()
    else:
        raise ValueError("unknown credentials")
