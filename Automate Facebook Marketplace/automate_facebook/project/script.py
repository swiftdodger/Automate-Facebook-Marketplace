import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Multilogin Browser setup
MULTILOGIN_API_KEY = 'your_multilogin_api_key'
BROWSER_PROFILE_ID = 'your_browser_profile_id'


def start_multilogin_browser(api_key, profile_id):
    options = Options()
    options.add_argument(f"--remote-debugging-port=9222")
    service = Service(executable_path="path_to_your_chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    # Connect to Multilogin Browser
    multilogin_url = f"http://localhost:35000/api/v2/profile/{profile_id}/start?automation=true"
    response = requests.get(multilogin_url, headers={"Authorization": f"Bearer {api_key}"})

    if response.status_code == 200:
        session_id = response.json()["value"]
        print(f"Multilogin session started with ID: {session_id}")
    else:
        print("Failed to start Multilogin session")
        driver.quit()
        return None

    return driver


def automate_facebook_listing(driver, listing_details):
    driver.get("https://www.facebook.com/marketplace/create/item")

    # Wait for the page to load
    time.sleep(5)

    # Log in (if necessary)
    email_elem = driver.find_element(By.ID, "email")
    password_elem = driver.find_element(By.ID, "pass")
    login_button = driver.find_element(By.NAME, "login")

    email_elem.send_keys("your_facebook_email")
    password_elem.send_keys("your_facebook_password")
    login_button.click()

    # Wait for login to complete
    time.sleep(10)

    # Fill out the listing form
    title_elem = driver.find_element(By.NAME, "title")
    price_elem = driver.find_element(By.NAME, "price")
    category_elem = driver.find_element(By.NAME, "category")
    description_elem = driver.find_element(By.NAME, "description")
    location_elem = driver.find_element(By.NAME, "location")

    title_elem.send_keys(listing_details["title"])
    price_elem.send_keys(listing_details["price"])
    category_elem.send_keys(listing_details["category"])
    description_elem.send_keys(listing_details["description"])
    location_elem.send_keys(listing_details["location"])

    # Upload an image
    image_elem = driver.find_element(By.NAME, "image")
    image_elem.send_keys(listing_details["image_path"])

    # Submit the form
    submit_button = driver.find_element(By.NAME, "submit")
    submit_button.click()

    # Wait for the listing to be posted
    time.sleep(10)


if __name__ == "__main__":
    listing_details = {
        "title": "Sample Rental Property",
        "price": "1200",
        "category": "Property Rentals",
        "description": "Spacious 2-bedroom apartment available for rent.",
        "location": "New York, NY",
        "image_path": "/path/to/image.jpg"
    }

    driver = start_multilogin_browser(MULTILOGIN_API_KEY, BROWSER_PROFILE_ID)

    if driver:
        automate_facebook_listing(driver, listing_details)
        driver.quit()
