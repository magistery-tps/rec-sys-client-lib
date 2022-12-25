from ..service    import ItemService
from django.utils import timezone
import logging

logging.basicConfig()
logging.getLogger('scheduler').setLevel(logging.INFO)


def update_items_stats_job():
    logging.info('Start to refresh items stats...')
    ItemService().refresh_popularity()
    logging.info('Finish to refresh items stats...')