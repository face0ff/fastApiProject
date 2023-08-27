from celery import Celery
import logging
# logging.basicConfig(level=logging.BASIC_FORMAT)


# def celery_app() -> Celery:
#
#     app = Celery(
#         'celery',
#         broker_url='amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost',
#         result_backend='rpc://',
#         include=['src.wallet.tasks']
#     )
#
#     app.conf.timezone = 'UTC'
#     app.conf.beat_schedule = {
#         'add-every-1-get-balance': {
#             'task': 'wallet.tasks.get_balance',
#             'schedule': 6,
#             'options': {'queue': 'get_balance'},
#             'args': ('0x18743AAF6D62dFbf309b78b4Ee3CBBc90f68D930',),
#         }
#     }
#
#     return app
#

# celery = celery_app()


app = Celery(
    'src.celery',
    broker_url='amqp://rabbit-user:1542@localhost:5672/rabbit-wallet-vhost',
    result_backend='rpc://',
    include=['src.wallet.tasks', 'src.parser.tasks']
)

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'add-every-1-get-wallet_list': {
        'task': 'src.wallet.tasks.get_wallet_list_task',
        'schedule': 60,
        'options': {'queue': 'get_wallet_list'},

    },
    # 'add-every-20-get-block_number': {
    #     'task': 'src.parser.tasks.get_block_number_task',
    #     'schedule': 30,
    #     'options': {'queue': 'block_number'},
    # }
}

app.autodiscover_tasks()

