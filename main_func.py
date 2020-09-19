from data import UOAScraper
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_uoa():
	scraper = UOAScraper()
	scraper.get_data()


def main():
	run_uoa()



if __name__ == "__main__":
    main()

	