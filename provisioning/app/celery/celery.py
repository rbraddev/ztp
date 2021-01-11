from celery import Celery


app = Celery(
    'celery',
    broker="amqp://guest:rabbitmq",
    include=["celery.tasks"]
)

if __name__ == '__main__':
    app.start()
