import httpx

from src.wallet.config_wallet import api_etherscan_url, api_etherscan
from fastapi import HTTPException, status

from src.wallet.containers import WalletContainer

w3 = WalletContainer.w3


async def get_balance(address=None):
    # address_list = await wallets()
    # print(address_list)

    headers = {
        "accept": "application/json",
    }
    params = {

        "action": "balancemulti",
        "address": address,
        "tag": "latest",
        "apikey": api_etherscan
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_etherscan_url}?module=account",
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            result = response.json()
            print(result['result'])
            balance = result['result'][0]['balance']
            return w3.from_wei(int(balance), 'ether')

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Проверьте все что вы ввели")
