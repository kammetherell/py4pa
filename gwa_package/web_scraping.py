import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_glassdoor_ratings():
    base_url = url = 'https://www.glassdoor.co.uk/Reviews/Experian-Reviews-E42406'
    reviews = []
    today = datetime.today().strftime('%Y-%m-%d')
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    #Overall Rating
    temp_url = base_url + '.htm'
    response = requests.get(temp_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Global Values
    country = 'Experian Global'
    rating = soup.find(
        'div',
        attrs={'class': 'common__EIReviewsRatingsStyles__ratingNum'}
    )
    num_reviews = soup.find(
        'div',
        attrs={'class': 'common__EIReviewSortBarStyles__sortsHeader'}
    )
    #Temporary Dictionary of values
    temp_dict = {
        'date': today,
        'country': country,
        'num_reviews': int(num_reviews.h2.span.strong.text),
        'rating': float(rating.text)
    }
    reviews.append(temp_dict)

    #Loop over all countries until no more found
    i=1
    keep_looping = True
    while keep_looping:
        temp_url = base_url + '-EI_IE42406.0,8_IL.9,23_IN' + str(i) + '.htm'
        response = requests.get(temp_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        country = soup.find(
            'div',
            attrs={'class': 'eiReviews__EIReviewsPageContainerStyles__EIReviewsPageContainer'}
        ).h1.text[9:-8]
        rating = soup.find(
            'div',
            attrs={'class': 'common__EIReviewsRatingsStyles__ratingNum'}
        )
        num_reviews = soup.find(
            'div',
            attrs={'class': 'common__EIReviewSortBarStyles__sortsHeader'}
        )

        if country == '':
            keep_looping = False
            i+=1
            continue

        if num_reviews is not None:
            print(i, country)
            temp_dict = {
                'date': today,
                'country': country,
                'num_reviews': int(num_reviews.h2.span.strong.text),
                'rating': float(rating.text)
            }

            reviews.append(temp_dict)

        i+=1
        continue

    return pd.DataFrame(reviews)
