from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sched import scheduler
import time


jobstores = {
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

scheduler.start()


def sampleFunc():
    print("called: %s" % time.ctime())


scheduler.add_job(sampleFunc, 'interval', seconds=10)

from flask import Flask
app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello, World!'

app.run(debug=False, host='0.0.0.0')
