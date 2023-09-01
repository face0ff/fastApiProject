from celery import Celery


app = Celery(
    'src.celery',
    broker_url='amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost',
    result_backend='rpc://',
    include=['src.wallet.tasks']
)

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'add-every-1-get-wallet_list': {
        'task': 'src.wallet.tasks.get_wallet_list_task',
        'schedule': 60,
        'options': {'queue': 'get_wallet_list'},

    },

}

app.autodiscover_tasks()

