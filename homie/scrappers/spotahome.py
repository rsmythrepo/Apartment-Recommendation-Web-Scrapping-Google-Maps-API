import re
import time
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

from .generics import Scrapper
class Spotahome(Scrapper):

    """
        Data about the webpage:
        - country: Spain
        - city: Barcelona
        - Service: Apartment rental agency in Barcelona
        """

    base_url = "https://www.spotahome.com/s/barcelona--spain/for-rent:apartments?utm_source=adwords&utm_medium=cpc&gad_source=1&gclid=CjwKCAiAlJKuBhAdEiwAnZb7lThqioNW05AloOH8yIisnJ-GUCFfSSy6S9RfT1VfmHibnfoZhkFPjhoCxW8QAvD_BwE&gclsrc=aw.ds"
    name = "Spotahome Barcelona"

    def get_links(self, base_url):

        links = []
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(base_url)
        time.sleep(3)

        # Click accept cookies
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        time.sleep(3)

        title = driver.find_element(By.CSS_SELECTOR, '.search-title__title').text.strip()
        number_of_apartments = title.split()[0]
        page_numbers = round(int(number_of_apartments) / 60)

        for page_number in range(page_numbers):
            apartments_listed = len(driver.find_elements(By.CSS_SELECTOR, '.l-list__item'))
            try:
                for i in range(1, apartments_listed + 1):
                    my_path = f"//*[@id='search-scroll']/div[2]/div[2]/div[{i}]/div/a"
                    link = driver.find_element(By.XPATH, my_path)
                    href = link.get_attribute("href")
                    links.append(href)

            except TimeoutException:
                print("Timed out waiting for apartment links.")
                continue

            try:
                xpath = f"//*[@id='search-scroll']/div[2]/div[3]/button[2]"
                next_page = driver.find_element(By.XPATH, xpath)
                next_page.click()
                time.sleep(1)

            except NoSuchElementException:
                print("Failed to find next page button.")
                break  # Exit loop if next page button is not found

            # TODO change to save/update in db
            df = pd.DataFrame(links)
            df = df.rename(columns={0: 'urls'})
            df.to_csv("../../Data/spotahome_links.csv")

        driver.quit()
