from bs4 import BeautifulSoup
import requests
import pandas as pd
import re 

# create soup object from goodreads url
def create_book_data(url):
    # extract the html content of the webpage
    goodreads_url = url
    book_page = requests.get(goodreads_url)

    # extract html content from the response object
    html_content = book_page.content
    book_data = BeautifulSoup(html_content, 'html.parser')

    # return the book data for scraping
    return book_data


def get_book_title(url):
    book_data = create_book_data(url)
    book_title = book_data.find('h1', attrs={'class':'Text Text__title1', 'data-testid':'bookTitle'}).get_text()
    return book_title