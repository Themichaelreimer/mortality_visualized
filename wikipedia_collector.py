import os, time
import requests

from typing import List
from bs4 import BeautifulSoup

BASE_PAGE = 'https://en.wikipedia.org/wiki/List_of_diseases_({})'
PAGES = '0-9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z'.split(',')
'''
    This script downloads a set of wikipedia pages.
    I think this set makes a reasonably complete list of diseases
'''


def get_page(url: str) -> str:
    ''' Returns a page's html '''
    time.sleep(4.0)
    page = requests.get(url)
    if page.status_code == 200:
        return page.text
    return ''


def is_link_valid(href: str) -> bool:
    # Nav Link
    if '#' in href:
        return False
    # Classes of articles that are likely to be linked, but we don't want
    if 'List_of_diseases' in href or 'Outline_of' in href or 'Category:' in href:
        return False
    # Articles that are linked but do not exist
    if 'redlink=1' in href:
        return False
    return True


def get_links_from_page(html: str) -> List[str]:
    ''' Returns a list of links from a page '''
    result = []
    soup = BeautifulSoup(html, features='html.parser')
    links = soup.find('div', {'id': 'content'}).findChildren('a')
    for link in links:
        href = link.get('href')
        if href and is_link_valid(href):
            result.append('https://en.wikipedia.org' + href)
    return result


def get_title(html: str) -> str:
    ''' Returns the title of an article '''
    soup = BeautifulSoup(html, features='html.parser')
    h1 = soup.find('h1', {'id': 'firstHeading'})
    if h1:
        return h1.text
    return ''


def save_webpage(name: str, html: str) -> None:
    ''' Saves html with a given file name '''
    path = os.path.join('data', 'wikipedia', name + '.html')
    with open(path, 'w+') as wiki_file:
        wiki_file.write(html)


def main() -> None:
    
    for PAGE_ID in PAGES:
        url = BASE_PAGE.format(PAGE_ID)
        index_html = get_page(url)
        links = get_links_from_page(index_html)

        for link in links:
            try:
                page_html = get_page(link)
                name = get_title(page_html)
                if name:
                    save_webpage(name, page_html)
            except Exception as e:
                print("===========================================")
                print(f"EXCEPTION ON LINK: <{link}>")
                print(e)
                print("===========================================")


if __name__ == "__main__":  
    main()
