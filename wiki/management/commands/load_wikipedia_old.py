from django.core.management.base import BaseCommand, CommandError
from wiki.models import *

import os
from bs4 import BeautifulSoup
from typing import List, Tuple

import wiki.business as business


class Command(BaseCommand):
    help = 'Loads wikipedia HTML into the articles table. Should run after wikipedia_collector.py'

    def handle(self, *args, **options):
        path = os.path.join('data', 'wikipedia')
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path,file)
            if os.path.isfile(file_path):
                try:
                    self.process_file(file_path)
                except Exception as e:
                    print(f'type({e}) - {e}')

    # This is the "main" function per file
    def process_file(self, fpath) -> None:
        '''
        Processes a file into an article object

        :param fpath: file path. Should be posix path, but string works too
        :return: None. Result is stored in DB
        '''

        with open(fpath, 'r') as f:
            html = f.read()

            soup = BeautifulSoup(html, features='html.parser')
            title = self.get_title(soup)
            first, text = self.get_text(soup)
            disease = self.process_infobox(soup, title)

            disease.print()

            article = {
                'title': title,
                'first_sentence': first,
                'disease': disease
            }

            business.create_article(article)


    @staticmethod
    def get_title(soup: BeautifulSoup) -> str:
        '''
        Gets the title of the article from the html
        :param soup: html soup
        :return: Title (str)
        '''
        h1 = soup.find('h1', {'id': 'firstHeading'})
        return h1.text


    @staticmethod
    def get_text(soup: BeautifulSoup) -> Tuple[str,str]:
        '''
        Gets the first sentence, and article text from html
        :param soup:
        :return: (first sentence, all sentences) as a tuple of strings
        '''
        paragraphs = soup.find_all('p')
        first = paragraphs[0].text
        text = ' '.join([p.text for p in paragraphs])
        return first, text


    @staticmethod
    def process_infobox(soup: BeautifulSoup, title:str):
        '''
        Looks for infoboxes on the page, and parses them into an infobox object - which is just
        a collection of data generally found in infoboxes

        :param soup:
        :return:
        '''
        data = {'name': title}
        tables = soup.find_all('table', {'class': 'infobox'})
        for table in tables:
            for row in table.findChildren('tr'):

                header = row.findChildren('th')
                if header:
                    header = header[0].text.lower()

                    if header == 'classification':
                        # Extracts ICD-10 class
                        text = row.text
                        toks = text.split('ICD')
                        if len(toks) > 1:
                            token = toks[1]
                            if ':' in token:
                                data['ICD-10'] = token.split(':')[1].strip()

                value = row.findChildren('td')
                if value:
                    value = value[0].text.lower()

                if header and value:
                    data[header] = value

        return business.handle_infobox(data)
