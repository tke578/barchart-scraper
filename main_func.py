from barchart import UOA
from orm import UOAMongo


def run_uoa():
	uoa = UOA()
	if uoa.data:
		mongo_client = UOAMongo()
		for uoa_obj in uoa.data:
			mongo_client.create_one(uoa_obj)

	else:
		print("No records found")


run_uoa()

	