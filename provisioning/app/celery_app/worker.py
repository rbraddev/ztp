from celery import Celery


celery_app = Celery(
    broker='amqp://guest@rabbitmq',
    include=('celery_app.tasks',)
)

celery_app.conf.update(
    task_routes = {
        'celery_app.tasks.provision': {
            'queue': 'provision'
        },
    }
)
