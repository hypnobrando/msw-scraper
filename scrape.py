from msw_scraper.msw_scraper import MSWScraper

SPOT = 'ocean-beach'

msw = MSWScraper(SPOT)
msw.scrape()
msw.savePlotNdays('out/' + SPOT + '.png', 0)
