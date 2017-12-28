from msw_scraper.msw_scraper import MSWScraper

SPOT = 'ocean-beach'

msw = MSWScraper(SPOT)
msw.scrape()
print(msw.scraped_data[0].data)
msw.savePlotNdays('out/' + SPOT + '.png', 0)
