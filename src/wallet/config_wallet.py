import os
import dotenv

dotenv.load_dotenv()

api_etherscan = os.getenv('API_ETHERSCAN')

api_moralis = os.getenv('API_MORALIS')

api_infura = os.getenv('API_INFURA')


api_moralis_url = 'https://deep-index.moralis.io/api/v2'

api_etherscan_url = 'https://api-sepolia.etherscan.io/api'

api_infura = f"https://sepolia.infura.io/v3/{api_infura}"
