
# Last edit: 5/25/2022
import os
import time
import urllib.request

import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd

# Finds a picture of the professor and writes link to csv file
def extract_images(site, first_name, last_name, dr, df, numProf):
    # Move to next link if it takes more than 2 seconds to connect
    # print("scanning for " + first_name + " " + last_name + " at link: " + site)
    try:
        dr.get(site)
    except:
        return

    images = driver.find_elements(By.TAG_NAME, 'img')
    for image in images:
        try:
            link = image.get_attribute("src")
            title = image.get_attribute("alt")
        except:
            continue

        if link is None:
            continue

        linkLower = link.lower()
        if title.lower().__contains__(last_name.lower()) and title.lower().__contains__(first_name.lower()):
            df.loc[numProf, 'Image'] = link
            print(link + " FOUND" + " " + last_name + ".")
            return True

        if linkLower.__contains__(last_name.lower() + ".jpg") or \
                linkLower.__contains__(first_name.lower() + "-" + last_name.lower()) or \
                linkLower.__contains__(last_name.lower() + ".png"):

            # write link to csv file
            df.loc[numProf, 'Image'] = link
            print(link + " FOUND" + " " + last_name + ".")
            return True

# Processes each professor in the list of test data
def process_professor(first, last, location, driver, df, numProf):
    url = 'https://google.com/search?q=' + first.replace(" ", "+") + '+' + last.replace(" ", "+") + '+' + location.replace(" ", "+")
    print(url)

    # Perform the request
    request = urllib.request.Request(url)

    # Set a normal User Agent header, otherwise Google will block the request.
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
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
    num = 0
    for div in divs:
        # From each search result, add the website link to links array
        if num > 4:
            break

        try:
            link = div.find('a').attrs['href']
        except:
            continue

        # This site will never have a picture of the professor
        if link.__contains__("ratemyprofessors"):
            continue
        else:
            links.append(link)
            num += 1

    # Extract images from each link
    for link in links:
        if extract_images(link, first.replace(" ", "-"), last.replace(" ", "-"), driver, df, numProf) is True:
            return 1

    # Write N\A to file if no image found
    df.loc[numProf, 'Image'] = "N\A"
    return 0

# This works perfectly, nothing to change
if __name__ == '__main__':
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Firefox(executable_path=r'C:\Users\jbrun\PycharmProjects\RPWebScraper\geckodriver.exe', options=options)
    driver.set_page_load_timeout(8)
    # process_professor("bilin", "zeng", "Bakersfield", driver)
    hits = 0
    df = pd.read_csv('testGroup.csv')
    print(df)
    with open('src/testGroup.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        rowStart = 0
        for row in csv_reader:
            if line_count < rowStart:
                line_count += 1
                continue
            if line_count > 0:
                hits += process_professor(row[0], row[1], row[6], driver, df, line_count - 1)
            df.to_csv(r"C:\Users\jbrun\Documents\testData.csv", index=False)
            line_count += 1
        print(f'Processed {line_count} professors.')
        print("" + hits + " matches in " + line_count + " professors")

