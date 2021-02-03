from celery import Celery


celery_app = Celery(broker="amqp://guest@rabbitmq", backend="redis://redis/0", include=("celery_app.tasks",))

celery_app.conf.update(
    task_routes={
        "celery_app.tasks.provision": {"queue": "provision"},
    },
    task_track_started=True,
)

celery_app.control.purge()
