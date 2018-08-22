from celery import Celery
from celery import task
from celery.utils.log import get_task_logger
from celery.decorators import periodic_task
import datetime
from status_page_config import StatusConfig
from state_page import StatusPage
from celery.schedules import crontab

config = StatusConfig('status_page_config.yaml')
app = Celery('task', backend = config.celery["backend"] , broker = config.celery["broker"], result_backend = config.celery["result_backend"])
page = StatusPage()

app.conf.timezone = 'UTC'

@periodic_task(run_every=crontab(minute=config.celery["interval"]))
def create_status_page():
    arr = []
    arr = page.select_data()
    print("arr")
    page.draw_image2(arr)
    page.generate_html(arr)