from ..service    import ItemService
from django.utils import timezone
import logging

logging.basicConfig()
logging.getLogger('scheduler').setLevel(logging.INFO)

item_service = ItemService()

def update_items_stats_job():
    logging.info('Start to refresh items stats...')
    item_service.refresh_stats()
    logging.info('Finish to refresh items stats...')