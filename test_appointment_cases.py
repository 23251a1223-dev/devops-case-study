import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class AppointmentSystemTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.binary_location = (
            r"C:\Users\gnits\AppData\Local\Google\Chrome\Application\chrome.exe"
        )
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(options=options)
        cls.url = "http://localhost:31979"

    def setUp(self):
        self.driver.get(self.url)

    def test_01_application_opens(self):
        self.assertEqual(
            self.driver.current_url.rstrip("/"),
            self.url
        )
        print("Application opened successfully")

    def test_02_page_title_exists(self):
        self.assertTrue(
            self.driver.title.strip(),
            "Page title should not be empty"
        )
        print("Page title test passed")

    def test_03_page_content_is_visible(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        self.assertTrue(
            body.is_displayed(),
            "Page body should be visible"
        )
        self.assertTrue(
            body.text.strip(),
            "Page should contain visible text"
        )
        print("Page content test passed")

    def test_04_page_has_no_browser_error(self):
        page_text = self.driver.find_element(
            By.TAG_NAME, "body"
        ).text.lower()

        self.assertNotIn("internal server error", page_text)
        self.assertNotIn("bad gateway", page_text)
        print("Browser error check passed")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
