import os
import dotenv

dotenv.load_dotenv()

broker_url = os.getenv('CELERY_BROKER_URL')
result_backend = os.getenv('CELERY_RESULT_BACKEND')

