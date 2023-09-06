from celery import Celery

from src.celery.config_celery import celery_broker_url, celery_result_backend

app = Celery(
    'src.celery',
    broker_url=celery_broker_url,
    result_backend=celery_result_backend,
    include=['src.wallet.tasks', 'src.ibay.tasks', 'src.users.tasks']
)

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'add-every-1-get-wallet_list': {
        'task': 'src.wallet.tasks.get_wallet_list_task',
        'schedule': 60,
        'options': {'queue': 'periodic'},

    },
    'add-every-5-get-delivery-order': {
            'task': 'src.ibay.tasks.get_last_delivery_order_task',
            'schedule': 5,
            'options': {'queue': 'periodic'},

        },

}

app.autodiscover_tasks()

