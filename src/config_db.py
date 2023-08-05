import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из файла .env

db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
