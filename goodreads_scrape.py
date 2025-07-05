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

def get_book_author(url):
    book_data = create_book_data(url)
    book_author = book_data.find('span', attrs={'class':'ContributorLink__name', 'data-testid': 'name'}).get_text()
    book_author = re.sub(r'\s+', ' ', book_author) # clean the author name for unnecessary space
    
    return book_author

def get_book_rating_data(url):
    book_data = create_book_data(url)
    book_rating_data = {"ave_rating":"", "rating_count":""} # create blank dict for book rating data
    book_rating_data['ave_rating'] = book_data.find('div', attrs={'class':'RatingStatistics__rating'}).get_text()
    book_rating_data['rating_count'] = book_data.find('span', attrs={'data-testid':'ratingsCount'}).get_text().split()[0]
    
    return book_rating_data

def get_ave_rating(url):
    book_rating_data = get_book_rating_data(url)
    book_ave_rating = book_rating_data['ave_rating']
    
    return book_ave_rating

def get_rating_count(url):
    book_rating_count_data = get_book_rating_data(url)
    book_rating_count = book_rating_count_data['rating_count']
    if ',' in book_rating_count:
        book_rating_count = book_rating_count.replace(',','')
    
    return book_rating_count

def get_book_desc(url):
    book_data = create_book_data(url)
    book_desc = book_data.find('span', attrs={'class':'Formatted'}).get_text()
    
    return book_desc

def get_book_cat(url):
    book_data = create_book_data(url)
    book_genres = []
    book_category_data_raw = book_data.find_all('span', attrs={'class':'BookPageMetadataSection__genreButton'}) # this will get all with the 'span' tag but only those related to the genre button
    
    for category in book_category_data_raw:
        data = category.find('span', attrs={'class':'Button__labelItem'}).get_text() # for each of the genre button need to extract only the genre and remove everything else
        book_genres.append(data)
    
    return book_genres

def get_pub_date(url):
    book_data = create_book_data(url)
    pub_details_raw = book_data.find('div', attrs={'class':'BookDetails'})
    pub_date_data = pub_details_raw.find('p', attrs={'data-testid':'publicationInfo'}).get_text() # from the book details, get only the detail related to the publication date
    pub_date_data = " ".join(pub_date_data.split()[2:]) # ommit the other strings and retain only the date of publication
    
    return pub_date_data

def book_details(url):
        book_info = {'title':'','author':'', 'description':'', 'category':[], 'date':'', 'ave_rating': None, 'rating_count': None}
        book_info['title'] = get_book_title(url)
        book_info['author'] = get_book_author(url)
        book_info['ave_rating'] = float(get_ave_rating(url))
        book_info['rating_count'] = int(get_rating_count(url))
        book_info['description'] = get_book_desc(url)
        book_info['category'] = get_book_cat(url)
        book_info['date'] = get_pub_date(url)

        return book_info