from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import matplotlib.pyplot as plt

from .day_data import DayData

class MSWScraper:
    def __init__(self, spot):
        self.QUALITY_MAP = {
            'background-danger': 0,
            'background-warning': 1,
            'background-success': 2
        }

        self.SPOTS = {
            'ocean-beach': 'https://magicseaweed.com/Ocean-Beach-Surf-Report/255/',
            'stinson-beach': 'https://magicseaweed.com/Stinson-Beach-Surf-Report/4216/',
            'pacifica': 'https://magicseaweed.com/Linda-Mar-Pacifica-Surf-Report/819/',
            'trestles': 'https://magicseaweed.com/Trestles-Surf-Report/291/',
            '36th-street-newport': 'https://magicseaweed.com/36th-St-Newport-Surf-Report/4683/',
            'blackies': 'https://magicseaweed.com/Blackies-Surf-Report/2575/'
        }

        if spot not in self.SPOTS:
            print(spot, 'not available')
            return

        url = self.SPOTS[spot]
        self.spot = spot

        response = urlopen(url).read().decode('utf-8')
        self.soup = BeautifulSoup(response, 'html.parser')

    def scrape(self):
        complete_data = []
        day = None
        day_data = []

        trs = self.soup.find('tbody').find_all('tr')
        for tr in trs:
            if 'class' not in tr.attrs:
                continue

            if 'msw-fc-date' in tr.attrs['class']:
                if len(day_data) != 0:
                    complete_data.append(DayData(day, day_data))

                day = tr.find('small').text
                day_data = []
                continue

            if 'msw-fc-primary' not in tr.attrs['class']:
                continue

            time = None
            height = None
            quality = None
            tds = tr.find_all('td')
            for td in tds:
                if 'class' not in td.attrs:
                    continue

                if 'row-title' in td.attrs['class']:
                    time_str = td.text.replace(" ", "")
                    if time_str == 'Noon':
                        time = 12
                    elif time_str[-2:] == 'am':
                        time = int(time_str[:-2]) % 12
                    elif time_str[-2:] == 'pm':
                        time = int(time_str[:-2]) % 12 + 12
                    continue

                if 'msw-fc-s' in td.attrs['class']:
                    height_data = td.text.replace(" ", "").split('-')
                    if len(height_data) == 1:
                        minAndMax = int(height_data[0].replace('ft', ''))
                        height = {
                            'min': minAndMax,
                            'max': minAndMax
                        }
                    else:
                        height = {
                            'min': int(height_data[0]),
                            'max': int(height_data[1].replace('ft', ''))
                        }

                if 'msw-fc-wa' in td.attrs['class']:
                    quality = None
                    for c in td.attrs['class']:
                        if 'background' in c:
                            quality = self.parse_quality(c.replace(" ", ""))
                            break

            day_data.append({'time': time, 'height': height, 'quality': quality})

        self.scraped_data = complete_data

    def parse_quality(self, raw):
        return self.QUALITY_MAP[raw]

    def savePlotNdays(self, outFile, ndays):
        if ndays >= len(self.scraped_data):
            print('ndays is too large')
            return

        fig, ax = plt.subplots()
        barPlot = ax.bar(self.scraped_data[ndays].times, self.scraped_data[ndays].avgHeights, 0.35)
        for i in range(len(self.scraped_data[ndays].data)):
            quality = self.scraped_data[ndays].qualities[i]
            barPlot[i].set_color(['red', 'orange', 'green', 'blue'][quality])

        # add some text for labels, title and axes ticks
        ax.set_title(self.spot + ' ' + self.scraped_data[ndays].day)
        ax.set_ylabel('Wave height (ft.)')
        maxHeight = max(self.scraped_data[ndays].avgHeights)
        ax.set_ylim(0, maxHeight * 1.25)
        ax.set_xlim(-1, 22)

        for rect in barPlot:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

        plt.savefig(outFile)
