from ..domain     import DomainContext
from django.utils import timezone
import logging

logging.basicConfig()
logging.getLogger('scheduler').setLevel(logging.INFO)


ctx = DomainContext()

def update_items_stats_job():
    logging.info('Start to refresh items stats...')
    ctx.item_service.refresh_stats()
    logging.info('Finish to refresh items stats...')