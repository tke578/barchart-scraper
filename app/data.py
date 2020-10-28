from datetime import datetime, time, date
from barchart import UOA
from orm import UOAMongo
from normalize import normalize_uoa_response
from utilities import Slack, retry, is_datestring_today
import logging



class UOAScraper:
	def __init__(self):
		self.mongo_client = UOAMongo()
		self.slack_client = Slack()

	@retry(Exception, tries=1)	
	def get_data(self):
		if MarketHours.is_market_open(datetime.now()):
			print('Scraper started')
			print(datetime.now())
			uoa = UOA(webdriver_path='/usr/local/bin/geckodriver')
			print('Scraper finished')
			print(datetime.now())
			print('Size of records')
			print(len(uoa.data))
			if uoa.data:
				logging.info('Scraper finished')
				records_to_post = []
				for uoa_obj in uoa.data:
					normalized_response = normalize_uoa_response(uoa_obj)
					if is_datestring_today(normalized_response['Last Trade']):
						records_to_post.append(normalized_response)
				recent_records = self._latest_posted_records()
				if len(records_to_post) > len(recent_records):
					self.mongo_client.remove(filter={"_id": { "$in": recent_records }})
					self.mongo_client.create_many(records_to_post)
			else:
				logging.warning('No results from scraper')


	def _latest_posted_records(self):
		start_time 	= datetime(date.today().year, date.today().month, date.today().day)
		end_time   	= datetime(date.today().year, date.today().month, date.today().day, 23, 59)
		records 	= self.mongo_client.find(filter={"created_at": { "$gt": start_time, "$lt": end_time }})
		object_ids 	= []
		for r in records:
			object_ids.append(r["_id"])
		return object_ids

class MarketHours:
	def is_market_open(date_time):
		holidays_2020 =  [date(2020,9,7), date(2020,11,26), date(2020,12,25)]
		holidays_2021 = [date(2021,1,1), date(2021,1,18), date(2021,2,15), date(2021,4,2), date(2021,5,31), date(2021,7,5), date(2021,9,6), date(2021,11,25), date(2021,12,24)]
		weekdays = [0,1,2,3,4]
		start = time(6,30,0)
		end = time(15,0,0)#buffer
		if date_time.date().year == 2020:
			holidays = holidays_2020
		else:
			holidays = holidays_2021
		if date_time.date() not in holidays and date_time.date().weekday() in weekdays:
			return start <= date_time.now().time() <= end
		print("Market is Closed")
		return False