from __future__ import absolute_import, unicode_literals
from multiprocessing import Process, Manager, Pool
from multiprocessing.managers import BaseManager, SyncManager
from celery import Celery
from celery import task
from celery.schedules import crontab
from celery.decorators import periodic_task
from datetime import timedelta
from check_cur import CheckData

check = CheckData([10 ** (-3), 5])
app = Celery()
app.conf.timezone = 'UTC'

class MyListManager(BaseManager):
    pass

MyListManager.register("syncarr")

class MyManager(SyncManager):
    pass

MyManager.register("syncdict")

@periodic_task(run_every=timedelta(seconds=3))
def task_found_error():
    manager = MyManager(address=('', 50000), authkey='abc'.encode())
    manager.connect()
    syncarr = manager.syncdict()
    print(syncarr)
    check.process_found_error(syncarr)

