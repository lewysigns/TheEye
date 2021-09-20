from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()
celery_url     = os.environ["CELERY_URL"]

celery = Celery(broker=celery_url)

