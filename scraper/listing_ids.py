import warnings
from selenium import webdriver
warnings.filterwarnings('ignore')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from webdriver_manager.chrome import ChromeDriverManager # type: ignore

options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--log-level=3")  # Suppresses INFO and WARNING logs

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.cars.com")
wait = WebDriverWait(driver, 5)

driver.execute_script("""
    const root = document.querySelector("#panel-19 > cars-search-form").shadowRoot;
    const selects = root.querySelectorAll("spark-select");

    // Helper to simulate user interaction on a dropdown input
    function simulateSelectInput(selectElem, value) {
        const input = selectElem.shadowRoot.querySelector("#input");
        input.focus();
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.blur();
    }

    if (selects[0]) simulateSelectInput(selects[0], 'used');  // Stock type
    if (selects[1]) simulateSelectInput(selects[1], 'all');   // Make
    if (selects[2]) simulateSelectInput(selects[2], '');      // Model (empty = All)
    if (selects[3]) simulateSelectInput(selects[3], 'all');   // Distance
    """)

time.sleep(5)

driver.execute_script("""
    const root = document.querySelector("#panel-19 > cars-search-form").shadowRoot;
    root.querySelector("spark-button").shadowRoot.querySelector("button").click();
    """)

html = driver.page_source

# Use BeautifulSoup to parse the page
soup = BeautifulSoup(html, 'html.parser')

page_values = []

# Extract from <spark-button> elements
buttons = soup.find_all('spark-button', {'phx-value-page': True})
for button in buttons:
    page_values.append(int(button['phx-value-page']))

# Extract from <a> elements
links = soup.find_all('a', {'phx-value-page': True})
for link in links:
    page_values.append(int(link['phx-value-page']))

# Find the highest number from the list and assign it to 'n'
n = max(page_values)

listing_ids = []

for i in range(1,n+1):
    # website in a variable
    website = 'https://www.cars.com/shopping/results/?makes[]=&maximum_distance=all&models[]=&page=' + str(i) + '&stock_type=used&zip='

    # Find all <a> tags with class 'vehicle-card-link'
    a_tags = soup.find_all('a', class_='vehicle-card-link')

    # Extract the 'data-listing-id' for each tag and store it in a list
    for tag in a_tags:
        listing_id = tag.get('data-listing-id')
        if listing_id:
            listing_ids.append(listing_id)