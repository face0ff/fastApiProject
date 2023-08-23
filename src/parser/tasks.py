# import asyncio
# from src.celery.celery import app
# from src.parser.utils import get_last_block_number
#
#
# @app.task()
# def get_block_number_task():
#     loop = asyncio.get_event_loop()
#     block_number = loop.run_until_complete(get_last_block_number())
#
