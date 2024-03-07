import logging

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from homie.scrappers.generics import Scrapper

logger = logging.getLogger("homie")

class HabitacliaScrapper(Scrapper):
    base_url = "https://www.habitaclia.com/alquiler-en-barcelones.htm"
    name = "Habitaclia"
    next_page_selector = "your_next_page_selector_here"

    def __init__(self, max_pages: int = 5):
        super().__init__(max_pages)

    def scrape(self):
        self.agent.get(self.base_url)
        self.sleep_randomly()
        self.sleep_randomly()
        # TODO Getting detected

        links = []

        # Agree to cookies
        try:
            agree_button = self.agent.find_element(By.ID, 'didomi-notice-agree-button')
            agree_button.click()
            self.sleep_randomly()
        except NoSuchElementException:
            self.sleep_randomly()
            self.sleep_randomly()
            print("No cookies notice found or already agreed.")
        except Exception as e:
            print("An error occurred while trying to agree to cookies:", e)

        df = pd.DataFrame(links)
        # Add your scraping logic here
        # Make sure to handle pagination if needed
        return df

    # Override initiate_driver method if needed to set specific options for this website
    def initiate_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Add additional options if needed

        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver


if __name__ == "__main__":
    # Configure logging if needed
    logging.basicConfig(level=logging.INFO)
    # Initialize and run the scrapper
    scrapper = HabitacliaScrapper(max_pages=5)
    df = scrapper.scrape()
    print(df.head())
