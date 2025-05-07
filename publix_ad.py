from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Set up Selenium with headless Chrome
options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Navigate to the Publix Weekly Ad "View All" page
driver.get('https://www.publix.com/savings/weekly-ad/view-all')
time.sleep(5)  # Wait for the page to load completely

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the Selenium driver
driver.quit()

# Find all product containers
product_cards = soup.find_all('div', class_='p-grid-item')

# List of target product keywords
target_products = ['Cupcake', 'Heineken', 'Tomatoes']

# Iterate through each product card
for card in product_cards:
    # Extract the product title
    title_tag = card.find('div', class_='title-wrapper')
    if title_tag:
        title_span = title_tag.find('span')
        if title_span:
            title = title_span.get_text(strip=True)
            # Check if the title matches any target product
            if any(product.lower() in title.lower() for product in target_products):
                # Extract the deal information
                deal_info = card.find('span', class_='p-text paragraph-sm normal context--default color--null')
                deal_text = deal_info.get_text(strip=True) if deal_info else 'No deal info'
                print(f"Product: {title}")
                print(f"Deal: {deal_text}")
                print('-' * 40)