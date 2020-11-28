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
		self.collection.insert_one(obj)

	def create_many(self, objs):
		self.collection.insert_many(objs)

	def find(self, filter={}):
		return self.collection.find(filter)

	def remove(self, filter={}):
		self.collection.remove(filter)

	def update_one(self, filter={}, obj={}):
		self.collection.update_one(filter, obj)

	def update_many(self, filter={}, obj={}):
		self.collection.update_many(filter, obj)