#Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

"""
Function to crawl a website and extract titles and URLs of posts.
Args:
    url (str): The URL of the website to crawl.
Returns:
    list: A list of tuples containing post titles and their corresponding URLs.
"""

def crawl_web(url):

    # Options for headless Chrome browser (If you want to run it in headless mode which is recommended for VMs)
    options = Options()
    options.binary_location = '/snap/bin/chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')

    # Path to your ChromeDriver
    chromedriver_path = '/usr/local/bin/chromedriver'
    service = Service(chromedriver_path)

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    #Empty list to store all titles and links
    all_titles_and_links = []
    
    # Loop through the first two pages of the website 
    for page_num in range(1, 3):
        
        # Construct the URL for each page
        if page_num == 1:
            full_url = url
        else:
            # Assuming the URL structure for pagination is like 'https://example.com/page/2'
            full_url = f"{url}/page/{page_num}"

        #Printing the URL being crawled
        print(f"Crawling: {full_url}")
        # Open the URL in the browser depending on the page number
        driver.get(full_url)

        # Wait for the page to load completely
        time.sleep(3)

        # Get the page source and parse it with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        # Find the main feed section this obviously changes from site to site because of the structure of the site
        main_feed = soup.find('section', class_='content-area')

        # Check if the main feed is found
        if not main_feed:
            # If not found, print a message and continue to the next page
            print(f"Main feed not found on page {page_num}.")
            continue
        # Find all post titles and links within the main feed
        post_titles = main_feed.find_all('h2', class_='entry-title')

        # For each post title, extract the text and link
        titles_and_links = [
            (title.a.text.strip(), title.a['href'])
            for title in post_titles if title.a
        ]
        #Add the titles and links to the list we use extend to add the new titles and links to the list from the other page
        all_titles_and_links.extend(titles_and_links)

    driver.quit()
    return all_titles_and_links


