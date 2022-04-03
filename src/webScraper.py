# Check very last set of comments to see where I left off
# Last edit: 4/3/2022 1:06pm

import urllib.request

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_images(site, last_name):
    # Move to next link if it takes more than 2 seconds to connect
    try:
        response = requests.get(site, timeout=2)
    except:
        return

    # initialize BeautifulSoup object for scraping data
    soup2 = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup2.find_all('img')

    # some website have no images, so 'src' key will throw error
    try:
        urls = [img['src'] for img in img_tags]
    except:
        urls = None

    # move to next link if no images data present
    if urls is None:
        return

    # iterate through each image url
    for url in urls:
        # only accept .jpg, .png, and .gif extensions
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
            continue

        # only take images that are of the author
        if not url.__contains__(last_name):
            continue

        # download image to cwd
        with open(filename.group(1), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)


if __name__ == '__main__':
    url = 'https://google.com/search?q=Shih+Lung+Woo+Los+Angeles'

    # Perform the request
    request = urllib.request.Request(url)

    # Set a normal User Agent header, otherwise Google will block the request.
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    raw_response = urllib.request.urlopen(request).read()

    # Read the repsonse as a standard utf-8 string
    html = raw_response.decode("utf-8")

    # initialize beautifulSoup object to read the html of the search
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the search result divs, skip all other divs
    divs = soup.select("#search div.g")

    # initialize links list
    links = []

    # Iterate through each search result
    for div in divs:
        # From each search result, add the website link to links array
        links.append(div.find('a').attrs['href'])

    # Extract images from each link
    for link in links:
        extract_images(link, "Woo")

    # import csv file => this is where I'm leaving off for today.
    # Tomorrow, implement algo to iterate through each author and pass in
    # name, city, and CSU/UC for search query
    listOfProfessors = pd.read_csv(r"C:\Users\jbrun\Downloads\testGroup.csv")
