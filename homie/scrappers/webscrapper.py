import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# Get the links for each apartment page on Idealista.com
def get_apartment_links_idealista(url):

    # TODO bypass captcha
    links = []
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    #driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    apts_links = driver.find_elements(By.CLASS_NAME, "item-info-container")
    for a in apts_links:
        links.append(a.find_element(By.CLASS_NAME, "item-link").get_attribute('href'))
    driver.quit()
    return apts_links

# Get the links for each apartment page on apartmentbarcelona.com
def get_apartment_links_ap_bcn(url):

    sub1 = "window.open('"
    sub2 = "');"
    s = str(re.escape(sub1))
    e = str(re.escape(sub2))
    links = []
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)
    driver.find_element(By.ID, 'btnCookieAgree').click()
    apts_links = driver.find_elements(By.CSS_SELECTOR, '.card.col-xs-12.pointer')
    time.sleep(3)
    for a in apts_links:
        string = a.find_element(By.CSS_SELECTOR, '.card-block.text-size-9').get_attribute('onclick')
        link = re.findall(s + "(.*)" + e, string)[0]
        links.append("https://www.apartmentbarcelona.com/" + link)

    # TODO click next page

    df = pd.DataFrame(links)
    df = df.rename(columns={0: 'urls'})
    # df.to_csv('urls_t.csv')
    driver.quit()
    return df


if __name__ == '__main__':

    # TODO how to bypass captcha
    idealista_url = "https://www.idealista.com/en/alquiler-viviendas/barcelona-barcelona/"
    # print(get_apartment_links_idealista(idealista_url))

    apartment_bcn_url = "https://www.apartmentbarcelona.com/es/alquileres-medio-largo-plazo/eur/?s=1"
    print(get_apartment_links_ap_bcn(apartment_bcn_url))

