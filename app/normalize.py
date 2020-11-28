from datetime import datetime
from utilities import is_a_datestring

def normalize_uoa_response(obj):
	return {
		"Symbol": 	obj.get('Symbol', None),
		"Price": 	float(obj.get('Price', 0).replace(',','')),
		"Type": 	obj.get('Type', None),
		"Strike": 	float(obj.get('Strike', 0).replace(',','')),
		"Exp Date": get_date(obj.get('Exp Date', None)),
		"DTE": 		float(obj.get('DTE', 0).replace(',','')),
		"Bid": 		float(obj.get('Bid', 0).replace(',','')),
		"Midpoint": float(obj.get('Midpoint', 0).replace(',','')),
		"Ask": 		float(obj.get('Ask', 0).replace(',','')),
		"Last": 	float(obj.get('Last', 0).replace(',','')),
		"Volume": 	int(obj.get('Volume',0).replace(',','')),
		"Open Int": int(obj.get('Open Int',0).replace(',','')),
		"Vol/OI": 	float(obj.get('Vol/OI', 0).replace(',','')),
		"IV": 		float(obj.get('IV',0).replace('%','')),
		"Last Trade": get_date(obj.get('Last Trade', None)),
		"created_at": datetime.now(),
		"updated_at": datetime.now()
	}


def get_date(date_string, date_format='%m/%d/%y %H:%M:%S'):
	is_a_valid_date_str = is_a_datestring(date_string)
	if not is_a_valid_date_str:
		return None
	time_string = f'{datetime.now().time().hour}:{datetime.now().time().minute}:{datetime.now().time().second}'
	return datetime.strptime(date_string + ' ' + time_string, date_format)




