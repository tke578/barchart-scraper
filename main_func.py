from data import UOAScraper


def run_uoa():
	scraper = UOAScraper()
	scraper.get_data()
	print('Scraper done')


def main():
	run_uoa()



if __name__ == "__main__":
    main()

	