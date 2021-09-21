from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()
celery_url     = os.environ["CELERY_URL"]
celery_backend = os.environ["RESULT_BACKEND"]

celery = Celery(broker=celery_url,result_backend=celery_backend)

