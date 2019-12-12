from flask import Flask
from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

from datetime import datetime
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler 
from apscheduler.triggers.interval import IntervalTrigger 

@app.before_first_request 
def initialize(): 
	scheduler = BackgroundScheduler() 
	scheduler.start() 
	scheduler.add_job(func=delete_old_records,	trigger=IntervalTrigger(hours=23))
	# Shut down the scheduler when exiting the app 
	atexit.register(lambda: scheduler.shutdown()) 

def delete_old_records(): 
	print('search old records...')
	for filename in os.listdir('./files/json/'):
		raw_date_from_name = filename.split('_')
		date_from_name = tuple(int(raw_date_from_name[i]) for i in range(7))
		if (datetime.now() - datetime(*date_from_name[0:7])).days > 1:
			os.remove('./files/json/{}'.format(filename))


