import os

from pymongo import MongoClient
from datetime import datetime

class UOAMongo:
	def __init__(self):
		host_string = os.environ['MONGO_URI']
		self.client = MongoClient(host_string)
		db = self.client['barchart']
		self.collection = db['uoa']

	def create_one(self,obj):
		obj.update(self.timestamps())
		self.collection.insert_one(obj)


	def timestamps(self):
		return {
			"created_at": datetime.now().strftime("%Y-%m-%d %I:%M:%S%p"),
			"updated_at": datetime.now().strftime("%Y-%m-%d %I:%M:%S%p")
		}