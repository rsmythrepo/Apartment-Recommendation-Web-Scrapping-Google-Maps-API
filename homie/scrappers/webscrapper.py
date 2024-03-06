import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

'''Using this as a working document'''

def get_data_spotahome(df_links):

    options = Options()
    driver = webdriver.Chrome(options=options)

    # Dictionary of apartment details
    data = {}

    # Go through apartment links and fetch the details
    for apartment_url in df_links['urls'][:5]:
        try:
            # Go to apartment url
            driver.get(apartment_url)
            time.sleep(1)

            # Get the cover image
            #image_url = driver.find_element(By.XPATH,"//*[@id='root']/div/section/div[1]/div[1]/div/div[2]/div[1]']").get_attribute("src")
            #print(image_url)
            #response = requests.get(image_url)
            #if response.status_code == 200:
            #    image = Image.open(BytesIO(response.content))

            title = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div[1]/div[3]/div[2]/span/h1').text.strip()
            price = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div[1]/div[3]/div[4]/div[2]/section/div/div/div[1]/div[1]/div[1]/p[2]').text.strip()
            deposit = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div[1]/div[3]/div[4]/div[2]/section/div/div/div[1]/div[2]/div[1]/p').text.strip()
            bathrooms = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div[1]/div[3]/div[2]/div[1]/span[3]/strong').text.strip()
            rooms = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div[1]/div[3]/div[2]/div[1]/span[2]/strong').text.strip()

            data[apartment_url] = {
                'title': title,
                'price': price,
                'deposit': deposit,
                'bathrooms': bathrooms,
                'rooms': rooms
            }
        except NoSuchElementException as e:
            print(f"Failed to extract details for apartment: {apartment_url}. Error: {e}")
            continue

    driver.quit()
    return data

if __name__ == '__main__':

    df_links = pd.read_csv("../../Data/spotahome_links.csv")
    print(get_data_spotahome(df_links))






