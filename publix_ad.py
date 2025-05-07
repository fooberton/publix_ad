from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

# List of target product keywords
target_products = ['Kodiak', 'chobani', 'protein', 'ratio yogurt']

# Set up headless Chrome
options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Navigate to the Publix Weekly Ad "View All" page
driver.get('https://www.publix.com/savings/weekly-ad/view-all')

# Wait for the initial content to load
wait = WebDriverWait(driver, 10)

while True:
    try:
        # Wait for the "Load More" button to be clickable
        load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.button-container > button')))
        load_more_button.click()
        #print("Clicked 'Load More' button.")
        # Wait for new content to load
        time.sleep(.2)
    except (TimeoutException, ElementClickInterceptedException):
        #print("No more 'Load More' button found or button not clickable.")
        break

# After all products are loaded, get the page source
html_content = driver.page_source
soup = BeautifulSoup(driver.page_source, 'html.parser')
# Close the browser
driver.quit()

# Find all product containers
product_cards = soup.find_all('div', class_='p-grid-item')



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

  
