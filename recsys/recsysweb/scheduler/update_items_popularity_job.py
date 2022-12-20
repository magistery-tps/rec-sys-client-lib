from ..service import ItemRecService
from django.utils import timezone
import logging

logging.basicConfig()
logging.getLogger('scheduler').setLevel(logging.INFO)


def update_items_popularity_job():
    logging.info('Start to refresh ite4ms popularity from user interactions...')
    ItemRecService().refresh_popularity()
    logging.info('Finish to refresh ite4ms popularity from user interactions...')