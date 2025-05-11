# scraper.py
import csv
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Function to create WebDriver instance (headless mode can be enabled)
def create_driver():
    options = Options()
    options.add_argument('--headless')  # Optional: for running in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# Scraping function for each vehicle
def scrape_vehicle(listing_id):
    driver = create_driver()
    vehicle_data = {}

    try:
        vehicle_url = f"https://www.cars.com/vehicledetail/{listing_id}"
        driver.get(vehicle_url)

        # Wait for the header to load and extract vehicle details
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "header.gallery-header")))
        header = driver.find_element(By.CSS_SELECTOR, "header.gallery-header")
        vehicle_data["Car name"] = header.find_element(By.CLASS_NAME, "listing-title").text
        vehicle_data["Car Price"] = header.find_element(By.CLASS_NAME, "primary-price").text
        vehicle_data["Car Price Badge"] = header.find_element(By.CSS_SELECTOR, 'span[data-qa="price-badge-text"]').text

        # Extract more details about the vehicle
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.sds-page-section.basics-section")))
        vehicle_data["Exterior Color"] = get_text(driver, "//dt[text()='Exterior color']/following-sibling::dd")
        vehicle_data["Drivetrain"] = get_text(driver, "//dt[text()='Drivetrain']/following-sibling::dd")
        vehicle_data["MPG"] = get_text(driver, "//dt[text()='MPG']/following-sibling::dd")
        vehicle_data["Fuel Type"] = get_text(driver, "//dt[text()='Fuel type']/following-sibling::dd")
        vehicle_data["Transmission"] = get_text(driver, "//dt[text()='Transmission']/following-sibling::dd")
        vehicle_data["Engine"] = get_text(driver, "//dt[text()='Engine']/following-sibling::dd")
        vehicle_data["VIN"] = get_text(driver, "//dt[text()='VIN']/following-sibling::dd")
        vehicle_data["Mileage"] = get_text(driver, "//dt[text()='Mileage']/following-sibling::dd")

        # Accident details
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.sds-page-section.vehicle-history-section")))
        accidents_or_damage = driver.find_element(By.XPATH, "//dt[text()='Accidents or damage']/following-sibling::dd").text
        vehicle_data["Accidents or Damage"] = "Yes" if "At least 1 accident or damage reported" in accidents_or_damage else "No"

        # Seller information
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.sds-page-section.seller-info")))
        vehicle_data["Seller Name"] = get_text(driver, ".seller-name")
        rating_element = driver.find_element(By.CSS_SELECTOR, "spark-rating")
        vehicle_data["Seller Rating"] = rating_element.get_attribute("rating") if rating_element else None
        vehicle_data["Seller Address"] = get_text(driver, ".dealer-address")

    except Exception as e:
        print(f"Error scraping {listing_id}: {e}")

    finally:
        driver.quit()

    return vehicle_data

# Helper function to safely get text from an element, returns None if not found
def get_text(driver, xpath_or_selector):
    try:
        element = driver.find_element(By.XPATH, xpath_or_selector) if xpath_or_selector.startswith("//") else driver.find_element(By.CSS_SELECTOR, xpath_or_selector)
        return element.text if element else None
    except Exception:
        return None

# Function to scrape all vehicles
def scrape_all(listing_ids):
    vehicle_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(scrape_vehicle, listing_ids)
        for result in results:
            if result:
                vehicle_data.append(result)
    return vehicle_data

# Import listing_ids from another file
from listing_ids import listing_ids

# Call the function to scrape data
data = scrape_all(listing_ids)

# Export the data to a CSV file
def export_to_csv(data, filename="data/raw/vehicle_data.csv"):
    if data:
        # Extract headers from the keys of the first dictionary in the list
        headers = data[0].keys()

        # Open CSV file in write mode
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()  # Write headers to CSV
            writer.writerows(data)  # Write data rows to CSV
        print(f"Data has been exported to {filename}")
    else:
        print("No data to export.")

# Export the scraped data to CSV
export_to_csv(data)

