#Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

"""
Function to scrape web content using Selenium and BeautifulSoup.
Args:
    url (str): The URL of the web page to scrape.
Returns:
    str: The extracted text content from the web page.
"""

def scrape_web(url):
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

    #Get the URL of the page to mine
    driver.get(url)

    #Print the URL of the page being mined
    print(f"\nScraping URL: {url}")
    
    # Wait for the page to load completely
    time.sleep(3)

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    #Find the main content of each post 
    content = soup.find('div', class_='entry-content')

    # Check if the content is found
    if not content:
        # If not found, print a message and return None
        print("Content not found.")
        return None

    # Extract the text from the content
    paragraphs = content.find_all('p')
    article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

    # Close the driver
    driver.quit()

    # Return the extracted text
    return article_text