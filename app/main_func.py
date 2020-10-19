import sys
from data import UOAScraper
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_uoa():

	try:
		scraper = UOAScraper()
		scraper.get_data()
		print('Scraper done')
	except:
		sys.exit()


def main():
	run_uoa()



if __name__ == "__main__":
    main()

	