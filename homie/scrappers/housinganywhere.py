import logging
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from homie.scrappers.generics import Scrapper

logger = logging.getLogger("homie")

class HousingAnywhereScrapper(Scrapper):
    base_url = "https://housinganywhere.com/s/London--United-Kingdom?categories=studio-for-rent%2Capartment-for-rent"
    name = "HousingAnywhere London"
    next_page_selector = "your_next_page_selector_here"

    def __init__(self, max_pages: int = 5):
        super().__init__(max_pages)

    def get_links(self):

        # Get Webpage
        self.agent.get(self.base_url)
        self.sleep_randomly()

        # Agree to cookies
        try:
            agree_button = self.agent.find_element(By.ID, 'onetrust-accept-btn-handler')
            agree_button.click()
            self.sleep_randomly()
        except NoSuchElementException:
            print("No cookies notice found or already agreed.")
        except Exception as e:
            print("An error occurred while trying to agree to cookies:", e)

        time.sleep(20)

        links = []

        # Get the links
        try:

            link_elements = self.agent.find_elements(By.CLASS_NAME, 'css-16pwyb1-cardLink-link')

            #TODO extract available date
            #details = self.agent.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div[3]/div/div/div[2]/div/div/div[2]/div[1]/a/div/div[2]/div[2]/div/span[4]')
            #print("prop details")
            #print(details.text)

            for link_element in link_elements:
                href = link_element.get_attribute('href')
                links.append(href)

        except NoSuchElementException:
            print("No links found")
        except Exception as e:
            print("An error occurred while getting links:", e)

        # Next page
        for i in range(2, 30):
            # Append the number to the base URL and add it to the list
            next_url = (f"{self.base_url}&page={i}")
            # Get Webpage
            self.agent.get(next_url)
            self.sleep_randomly()

            try:
                agree_button = self.agent.find_element(By.ID, 'onetrust-accept-btn-handler')
                agree_button.click()
                self.sleep_randomly()
            except NoSuchElementException:
                print("No cookies notice found or already agreed.")
            except Exception as e:
                print("An error occurred while trying to agree to cookies:", e)

            time.sleep(15)

            # Get the links
            try:
                link_elements = self.agent.find_elements(By.CLASS_NAME, 'css-16pwyb1-cardLink-link')
                print(link_elements)
                for link_element in link_elements:
                    href = link_element.get_attribute('href')
                    links.append(href)

            except NoSuchElementException:
                print("No links found")
            except Exception as e:
                print("An error occurred while getting links:", e)

        self.sleep_randomly()
        df = pd.DataFrame(links)
        df = df.rename(columns={0: 'urls'})
        df.to_csv("../../Data/raw/apartmentsanywhere_links2.csv")
        self.agent.quit()
        return links


    def get_data(self):

        # TODO change to get links from db
        df_links = pd.read_csv("../../Data/raw/apartmentsanywhere_links.csv")

        # Dictionary of apartment details
        data = {}

        # Go through apartment links and fetch the details
        for apartment_url in df_links['urls']:
            try:
                # Go to apartment url
                self.agent.get(apartment_url)
                self.sleep_randomly()

                try:
                    agree_button = self.agent.find_element(By.ID, 'onetrust-accept-btn-handler')
                    agree_button.click()
                    self.sleep_randomly()
                except NoSuchElementException:
                    print("No cookies notice found or already agreed.")
                except Exception as e:
                    print("An error occurred while trying to agree to cookies:", e)

                # TODO Get the cover image
                #image_element = self.agent.find_element(By.XPATH, "//div[@class='cover-img jsPhotosApartment']").get_attribute( "style")
                #image_url = image_element.split('("', 1)[1].split('")')[0]
                #response = requests.get(image_url)
                #if response.status_code == 200:
                #    image = Image.open(BytesIO(response.content))

                # Get apartment details
                address = self.agent.find_element(By.CLASS_NAME, "MuiTypography-root.MuiTypography-h2.css-1njgbqb-h2-overflow-initial-color-default-address").text.strip()
                address += ", London"

                apartment_details = self.agent.find_elements(By.CLASS_NAME, "MuiGrid-root.MuiGrid-item.css-1e5azn1-highlightItem")
                house_type = apartment_details[0].text.strip()
                dimensions = apartment_details[1].text.strip()
                furnish_type = apartment_details[2].text.strip()
                try:
                    bedrooms = apartment_details[4].text.strip()
                except:
                    bedrooms = apartment_details[3].text.strip()

                min_tenancy = self.agent.find_element(By.XPATH, '//*[@id="rental-conditions"]/div/div/div/div[2]/div/div[2]').text.strip()
                deposit = self.agent.find_element(By.XPATH, '//*[@id="rental-conditions"]/div/div/div/div[3]/div/div[2]').text.strip()
                price_pm = self.agent.find_element(By.CLASS_NAME, "MuiGrid-root.MuiGrid-container.MuiGrid-item.MuiGrid-grid-xs-6.css-174xb6y-costName").text.strip()
                price_pw = 0
                let_type = "Long term"

                #TODO need to get from main page
                let_available_date = "now"

                facilities = self.agent.find_elements(By.CLASS_NAME, "MuiGrid-root.MuiGrid-item.css-ze4t1g-availableFacilities")
                bathrooms = 0
                for facility in facilities:
                    if "Toilet" in facility.text.strip():
                        bathrooms += 1
                    elif "toilet" in facility.text.strip():
                        bathrooms += 1
                    elif "bathroom" in facility.text.strip():
                        bathrooms += 1
                    elif "Bathroom" in facility.text.strip():
                        bathrooms += 1

                description = self.agent.find_element(By.CLASS_NAME, 'css-1lzqrt-preWrap-breakWord-description').text.strip()


                data[apartment_url] = {
                    'address': address,
                    'price_per_month': price_pm,
                    'price_per_week': price_pw,
                    'let_available_date': let_available_date,
                    'deposit': deposit,
                    'min_tenancy': min_tenancy,
                    'furnish_type': furnish_type,
                    'let_type': let_type,
                    'house_type': house_type,
                    'bedrooms': bedrooms,
                    'bathrooms': bathrooms,
                    'dimensions': dimensions,
                    'description': description
                }
            except NoSuchElementException as e:
                print(f"Failed to extract details for apartment: {apartment_url}. Error: {e}")
                continue

        self.agent.quit()
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(data.values(), index=data.keys())
        df.to_csv("../../Data/raw/housinganywhere_data.csv")

        return data

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
    scrapper = HousingAnywhereScrapper(max_pages=5)
    #links = scrapper.get_links()
    #print(links)
    #print(len(links))
    #print(df.head())
    #print(df.shape)
    #print(df['urls'].iloc[0])

    data = scrapper.get_data()
    print(data)
