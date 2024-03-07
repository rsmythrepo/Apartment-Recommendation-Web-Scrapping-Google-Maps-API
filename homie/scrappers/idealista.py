import logging

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from homie.scrappers.generics import Scrapper

logger = logging.getLogger("homie")

class IdealistaScrapper(Scrapper):
    base_url = "https://www.idealista.com/venta-viviendas/barcelona-barcelona/"
    name = "Idealista"
    next_page_selector = "your_next_page_selector_here"

    def __init__(self, max_pages: int = 5):
        super().__init__(max_pages)

    def scrape(self):

        # Go to website
        self.sleep_randomly()
        self.agent.get(self.base_url)
        self.sleep_randomly()

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


        # Get links
        try:
            link_elements = self.agent.find_elements(By.CSS_SELECTOR, 'a.item-link')
            self.sleep_randomly()
            for link_element in link_elements:
                href = link_element.get_attribute('href')
                links.append(href)

        except NoSuchElementException:
            print("No links found.")

        df = pd.DataFrame(links)
        df = df.rename(columns={0: 'urls'})

        return df

    # Override initiate_driver method if needed to set specific options for this website
    def initiate_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver


if __name__ == "__main__":
    # Configure logging if needed
    logging.basicConfig(level=logging.INFO)
    # Initialize and run the scrapper
    scrapper = IdealistaScrapper(max_pages=5)
    df = scrapper.scrape()
    print(df.head())
