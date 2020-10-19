from flask import Flask, jsonify, request
from data import UOAScraper
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)



@app.route('/', methods=['GET'])
def hello():
	return "Time is running out!"


#@app.route('/run_uoa', methods=['GET'])
def run_uoa():
	scraper = UOAScraper()
	scraper.get_data()
	return 'Scraper done'

sched = BackgroundScheduler(daemon=True)
sched.add_job(run_uoa,'interval',minutes=15)
sched.start()


if __name__ == '__main__':
    app.run(host="0.0.0.0")