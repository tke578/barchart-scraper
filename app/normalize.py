from datetime import datetime

def normalize_uoa_response(obj):
	return {
		"Symbol": 	obj.get('Symbol', None),
		"Price": 	float(obj.get('Price', 0).replace(',','')),
		"Type": 	obj.get('Type', None),
		"Strike": 	float(obj.get('Strike', 0).replace(',','')),
		"Exp Date": obj.get('Exp Date', None),
		"DTE": 		float(obj.get('DTE', 0).replace(',','')),
		"Bid": 		float(obj.get('Bid', 0).replace(',','')),
		"Midpoint": float(obj.get('Midpoint', 0).replace(',','')),
		"Ask": 		float(obj.get('Ask', 0).replace(',','')),
		"Last": 	float(obj.get('Last', 0).replace(',','')),
		"Volume": 	int(obj.get('Volume',0).replace(',','')),
		"Open Int": int(obj.get('Open Int',0).replace(',','')),
		"Vol/OI": 	float(obj.get('Vol/OI', 0).replace(',','')),
		"IV": 		float(obj.get('IV',0).replace('%','')),
		"Last Trade": obj.get('Last Trade', None),
		"created_at": datetime.now(),
		"updated_at": datetime.now()
	}