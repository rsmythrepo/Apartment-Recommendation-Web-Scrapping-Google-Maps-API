import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
from homie.scrappers.generics import Scrapper
from selenium import webdriver
from selenium.webdriver.common.by import By

logger = logging.getLogger("homie")

class RightMoveScrapper(Scrapper):
    base_url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93917&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords="
    name = "RightMove London"
    next_page_selector = "your_next_page_selector_here"

    def __init__(self, max_pages: int = 5):
        super().__init__(max_pages)

    def get_links(self):

        # Get Webpage
        self.agent.get(self.base_url)
        self.sleep_randomly()

        links = []

        # Fetch the first pages elements
        try:
            link_elements = self.agent.find_elements(By.CSS_SELECTOR, 'a.propertyCard-link.property-card-updates')
            for link_element in link_elements:
                href = link_element.get_attribute('href')
                links.append(href)
        except NoSuchElementException:
            print("No links found.")

        # Next page
        try:
            next_button = self.agent.find_element(By.CLASS_NAME,
                                                  'pagination-button.pagination-direction.pagination-direction--next')
            next_button.click()
            print("Clicked on the next button.")
        except NoSuchElementException:
            print("Next button not found.")

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

        for x in range(41):
            self.sleep_randomly()

            # Get links
            try:
                link_elements = self.agent.find_elements(By.CSS_SELECTOR, 'a.propertyCard-link.property-card-updates')
                for link_element in link_elements:
                    href = link_element.get_attribute('href')
                    links.append(href)
            except NoSuchElementException:
                print("No links found.")

            # Go to next page
            try:
                next_button = self.agent.find_element(By.CLASS_NAME, 'pagination-button.pagination-direction.pagination-direction--next')
                next_button.click()
                print("Clicked on the next button.")
                self.sleep_randomly()
            except NoSuchElementException:
                print("Next button not found.")

        df = pd.DataFrame(links)
        df = df.rename(columns={0: 'urls'})
        df.to_csv("../../Data/rightmoves_links.csv")
        self.agent.quit()
        return df


    def get_data(self):

        # TODO change to get links from db
        df_links = pd.read_csv("../../Data/raw/rightmoves_links.csv")

        # Dictionary of apartment details
        data = {}

        # Go through apartment links and fetch the details
        for apartment_url in df_links['urls']:
            try:
                # Go to apartment url
                self.agent.get(apartment_url)
                self.sleep_randomly()

                # TODO Get the cover image
                # image_element = self.agent.find_element(By.XPATH, "//div[@class='cover-img jsPhotosApartment']").get_attribute( "style")
                # image_url = image_element.split('("', 1)[1].split('")')[0]
                # response = requests.get(image_url)
                # if response.status_code == 200:
                #    image = Image.open(BytesIO(response.content))

                # Get apartment details
                address = self.agent.find_element(By.CSS_SELECTOR, 'div._1KCWj_-6e8-7_oJv_prX0H h1._2uQQ3SV0eMHL1P6t5ZDo2q').text.strip()
                price_pm = self.agent.find_element(By.CSS_SELECTOR, 'div._1gfnqJ3Vtd1z40MlC0MzXu span').text.strip()
                price_pw = self.agent.find_element(By.CSS_SELECTOR, 'div.HXfWxKgwCdWTESd5VaU73').text.strip()

                letting_details = self.agent.find_element(By.CLASS_NAME, '_2E1qBJkWUYMJYHfYJzUb_r')
                list_letting_details = letting_details.find_elements(By.CLASS_NAME, '_2RnXSVJcWbWv4IpBC1Sng6')

                let_available_date = list_letting_details[0].find_element(By.TAG_NAME, 'dd').text.strip()
                deposit = list_letting_details[1].find_element(By.TAG_NAME, 'dd').text.strip()
                min_tenancy = list_letting_details[2].find_element(By.TAG_NAME, 'dd').text.strip()
                let_type = list_letting_details[3].find_element(By.TAG_NAME, 'dd').text.strip()
                furnish_type = list_letting_details[4].find_element(By.TAG_NAME, 'dd').text.strip()

                apartment_details = self.agent.find_element(By.CLASS_NAME, '_4hBezflLdgDMdFtURKTWh')
                list_apartment_details = apartment_details.find_elements(By.CLASS_NAME, '_3gIoc-NFXILAOZEaEjJi1n')

                house_type = list_apartment_details[0].find_element(By.TAG_NAME, 'dd').text.strip()
                bedrooms = list_apartment_details[1].find_element(By.TAG_NAME, 'dd').text.strip()
                try:
                    bathrooms = list_apartment_details[2].find_element(By.TAG_NAME, 'dd').text.strip()
                except:
                    bathrooms = "Ask Agent"
                try:
                    dimensions = list_apartment_details[3].find_element(By.TAG_NAME, 'dd').text.strip()
                except:
                    dimensions = "Ask Agent"

                description = self.agent.find_element(By.CLASS_NAME, 'STw8udCxUaBUMfOOZu0iL').text.strip()

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
        df.to_csv("../../Data/rightmoves_data.csv")

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
    scrapper = RightMoveScrapper(max_pages=5)
    #df = scrapper.get_links()
    #print(df.head())
    #print(df.shape)
    #print(df['urls'].iloc[0])

    data = scrapper.get_data()
    print(data)