import asyncio
import loguru
from src.celery.celery import app
from src.wallet.wallet_utils import transaction_search, transaction_save, wallet_search


@app.task()
def search_transaction_in_block_task(body):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(transaction_search.transaction_ws_search(body))


# @app.task()
# def get_wallet_search_task(body):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(wallet_search.wallets_search(body))


@app.task(autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=10, max_retries=5)
def get_transaction_search_task(body):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(transaction_search.transaction_search(body))

    if result is False:
        raise Exception("transaction_search returned False")


# @app.task(bind=True, max_retries=5)
# def get_transaction_search_task(self, body):
#     try:
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(transaction_search.transaction_search(body))
#     except Exception as exc:
#         countdown = 3
#         raise self.retry(exc=exc, countdown=countdown)


@app.task()
def get_wallet_list_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wallet_search.get_wallet_list())




# @app.task()
# def get_wallet_lost_task(body):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(wallet_search.wallets_lost(body))


# @app.task()
# def get_transaction_search_task(body):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(transaction_search.transaction_search(body))


@app.task()
def save_transaction_task(body):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(transaction_save.transaction_save(body))


