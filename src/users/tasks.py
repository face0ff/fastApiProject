import asyncio

import loguru

from src.celery.celery import app
from src.users.containers import UserContainer


@app.task()
def save_chat_task(email):
    loguru.logger.critical('TASK')
    request = UserContainer.user_request()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(request.save_chat(email))


