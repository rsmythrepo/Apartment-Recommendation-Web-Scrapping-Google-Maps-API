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
class ApartmentBCN(Scrapper):

    """
        Data about the webpage:
        - country: Spain
        - city: Barcelona
        - Service: Apartment rental agency in Barcelona
        """

    base_url = "https://www.apartmentbarcelona.com/es/alquileres-medio-largo-plazo/eur/?s=1"
    name = "AB Apartment Barcelona"
    def get_links(self, base_url):
        sub1 = "window.open('"
        sub2 = "');"
        s = str(re.escape(sub1))
        e = str(re.escape(sub2))
        links = []

        options = Options()
        driver = webdriver.Chrome(options=options)

        try:
            # Go to website
            driver.get(base_url)

            # Agree to cookies
            driver.find_element(By.ID, 'btnCookieAgree').click()

            # Go through the pages and grab the apartment links
            for page_number in range(2, 12):
                try:
                    time.sleep(3)
                    apts_links = driver.find_elements(By.CSS_SELECTOR, '.card.col-xs-12.pointer')
                    for a in apts_links:
                        try:
                            string = a.find_element(By.CSS_SELECTOR, '.card-block.text-size-9').get_attribute('onclick')
                            link = re.findall(s + "(.*)" + e, string)[0]
                            links.append("https://www.apartmentbarcelona.com/" + link)
                        except NoSuchElementException:
                            print("Failed to extract link for apartment.")
                            continue
                except TimeoutException:
                    print("Timed out waiting for apartment links.")
                    continue

                try:
                    time.sleep(3)
                    xpath = f"//ul[@id='paginator-container']/li/a[@data-page='{page_number}']"
                    next_page = driver.find_element(By.XPATH, xpath)
                    next_page.click()
                except NoSuchElementException:
                    print("Failed to find next page button.")
                    break  # Exit loop if next page button is not found

            #TODO change to save/update links and apartment ids in db
            # Export the links to CSV
            df = pd.DataFrame(links)
            df = df.rename(columns={0: 'urls'})
            df.to_csv("../../Data/ap_bcn_links.csv")
            return

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()

    def get_data(self):

        # TODO change to get links from db
        df_links = pd.read_csv("../../Data/ap_bcn_links.csv")
        options = Options()
        driver = webdriver.Chrome(options=options)

        # Dictionary of apartment details
        data = {}

        # Go through apartment links and fetch the details
        for apartment_url in df_links['urls']:
            try:
                # Go to apartment url
                driver.get(apartment_url)
                time.sleep(3)

                # Get the cover image
                image_element = driver.find_element(By.XPATH,
                                                    "//div[@class='cover-img jsPhotosApartment']").get_attribute("style")
                image_url = image_element.split('("', 1)[1].split('")')[0]
                response = requests.get(image_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))

                # Get apartment details
                title = driver.find_element(By.ID, 'nameApartment').text.strip()
                district = driver.find_element(By.ID, 'DistrictInfo').text.strip()
                price = driver.find_element(By.ID, 'priceMonthDetail').text.strip()
                deposit = driver.find_element(By.ID, 'depositMonthDetail').text.strip()
                bathrooms = driver.find_element(By.ID, 'LavaboInfo').text.strip()
                dimensions = driver.find_element(By.ID, 'MetrosInfo').text.strip()
                rooms = driver.find_element(By.ID, 'HabitacionesInfo').text.strip()
                floor = driver.find_element(By.ID, 'PisoInfo').text.strip()
                description = driver.find_element(By.ID, 'dvDescripcionApt').text.strip()

                data[apartment_url] = {
                    'image': image,
                    'title': title,
                    'district': district,
                    'price': price,
                    'deposit': deposit,
                    'bathrooms': bathrooms,
                    'dimensions': dimensions,
                    'rooms': rooms,
                    'floor': floor,
                    'description': description
                }
            except NoSuchElementException as e:
                print(f"Failed to extract details for apartment: {apartment_url}. Error: {e}")
                continue

        driver.quit()
        return data

    #TODO save the data in a db
    def save_data(self, data) -> None:
        """
        Save the data into the db
        """