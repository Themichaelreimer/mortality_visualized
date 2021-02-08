from django.core.management.base import BaseCommand, CommandError
from wiki.models import *

import os
from bs4 import BeautifulSoup
from typing import List, Tuple


class Command(BaseCommand):
    help = 'Loads wikipedia HTML into the articles table. Should run after wikipedia_collector.py'

    def handle(self, *args, **options):
        path = os.path.join('data','wikipedia')
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path,file)
            if os.path.isfile(file_path):
                self.process_file(file_path)

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
            import pdb
            pdb.set_trace()

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
    def get_infobox(soup: BeautifulSoup) -> Infobox:
        '''
        Looks for infoboxes on the page, and parses them into an infobox object - which is just
        a collection of data generally found in infoboxes

        :param soup:
        :return:
        '''