from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution
import sys
from .update_items_popularity_job import update_items_popularity_job


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    scheduler.add_job(update_items_popularity_job, 'interval', minutes=1, max_instances=1, id='update_items_popularity_job', replace_existing=True)
    
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)