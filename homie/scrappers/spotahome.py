import logging
import time

import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from homie.scrappers.generics import Scrapper

logger = logging.getLogger("homie")
class SpotahomeScrapper(Scrapper):

    """
        Data about the webpage:
        - country: Spain
        - city: Barcelona
        - Service: Apartment rental agency in Barcelona
        """

    base_url = "https://www.spotahome.com/s/london--uk"
    #base_url = "https://www.spotahome.com/s/barcelona--spain/for-rent:apartments?utm_source=adwords&utm_medium=cpc&gad_source=1&gclid=CjwKCAiAlJKuBhAdEiwAnZb7lThqioNW05AloOH8yIisnJ-GUCFfSSy6S9RfT1VfmHibnfoZhkFPjhoCxW8QAvD_BwE&gclsrc=aw.ds"
    name = "Spotahome Barcelona"
    next_page_selector = "your_next_page_selector_here"

    def get_links(self):

        links = []
        options = Options()
        self.sleep_randomly()
        self.agent.get(self.base_url)
        self.sleep_randomly()
        time.sleep(3)

        # Click accept cookies
        self.agent.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(3)

        title = self.agent.find_element(By.CSS_SELECTOR, '.search-title__title').text.strip()
        number_of_apartments = title.split()[0]
        page_numbers = round(int(number_of_apartments) / 60)

        for page_number in range(page_numbers):
            apartments_listed = len(self.agent.find_elements(By.CSS_SELECTOR, '.l-list__item'))
            try:
                for i in range(1, apartments_listed + 1):
                    my_path = f"//*[@id='search-scroll']/div[2]/div[2]/div[{i}]/div/a"
                    link = self.agent.find_element(By.XPATH, my_path)
                    href = link.get_attribute("href")
                    links.append(href)

            except TimeoutException:
                print("Timed out waiting for apartment links.")
                continue

            try:
                xpath = "//*[@id='search-scroll']/div[2]/div[3]/button[2]"
                next_page = self.agent.find_element(By.XPATH, xpath)
                next_page.click()
                time.sleep(1)

            except NoSuchElementException:
                print("Failed to find next page button.")
                break  # Exit loop if next page button is not found

            # TODO change to save/update in db
        df = pd.DataFrame(links)
        df = df.rename(columns={0: 'urls'})
            #df.to_csv("../../Data/spotahome_links.csv")

        self.agent.quit()
        return df

if __name__ == "__main__":
    # Configure logging if needed
    logging.basicConfig(level=logging.INFO)
    # Initialize and run the scrapper
    scrapper = SpotahomeScrapper(max_pages=5)
    df = scrapper.get_links()
    print(df.head())
    print(df['urls'].iloc[0])
