import sys
from data import UOAScraper


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

	