import os
import time
from random import randint

from fbtftp.base_handler import ResponseData
from fbtftp.base_handler import StringResponseData

from config import Config
from celery_app.worker import celery_app
from celery_app.tasks import provision
from core.utils import render_file


class FileResponseData(ResponseData):
    def __init__(self, path):
        self._size = os.stat(path).st_size
        self._reader = open(path, "rb")

    def read(self, n):
        return self._reader.read(n)

    def size(self):
        return self._size

    def close(self):
        self._reader.close()


def handle_request(root: str, file: str, host: str):
    c = Config()

    if file == 'network-confg':
        config = render_file(
            './templates/config',
            file, username=c.credentials["provision"]["username"],
            password=c.credentials["provision"]["password"],
            host=host[0]
        )
        return StringResponseData(config)
    elif os.path.exists(os.path.join(root, file)):
        return FileResponseData(os.path.join(root, file))    
    else:
        return None


def handle_session(stats):
    if stats.packets_sent > 0:
        time.sleep(randint(0.0, 5.0))
        print(f"{stats.peer[0]} received {stats.file_path}")

        task_id = f"{stats.peer[0]}-{stats.file_path}"
        task = celery_app.AsyncResult(task_id)
        if task.state in ["FAILED", "SUCCESS"]:
            task.forget()
            task = provision.apply_async(task_id=task_id)
            print(task.id)
        elif task.state == "PENDING":
            task = provision.apply_async(task_id=task_id)
            print(task.id)
        else:
            print(f"{task_id} is currently running")
