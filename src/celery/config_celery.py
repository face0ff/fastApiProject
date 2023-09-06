import os
import dotenv

dotenv.load_dotenv()


celery_broker_url = os.getenv('CELERY_BROKER_URL')
celery_result_backend = os.getenv('CELERY_RESULT_BACKEND')
