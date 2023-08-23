# import asyncio
#
# import celery
# import httpx
# from web3 import Web3
# from fastapi import HTTPException, status, Response
# from fastapi import APIRouter, Depends
# from dependency_injector.wiring import inject, Provide
#
# from src.celery.celery import app
# from src.wallet.config_wallet import api_etherscan_url, api_etherscan
# from src.wallet.utils import get_balance
#
#
# @app.task()
# def get_balance_task():
#     loop = asyncio.get_event_loop()
#     balance = loop.run_until_complete(get_balance())
#     print(balance)
