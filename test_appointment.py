
from selenium import webdriver
from selenium.webdriver.common.by import By

# Open Chrome
driver = webdriver.Chrome()

try:
    # Open the application running on Kubernetes
    driver.get("http://localhost:31979")

    # Display the page title and URL
    print("Page title:", driver.title)
    print("Application URL:", driver.current_url)

    # Verify that the page loaded
    assert driver.current_url.startswith("http://localhost:31979")
    print("TEST PASSED: Application opened successfully")

finally:
    driver.quit()
