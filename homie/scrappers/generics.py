from db.models import Flat
from selenium import webdriver
import time
import random


class Scrapper:
    base_url = ""
    name = ""
    robots = ""  # url to the robots.txt file

    next_page_selector = "li.next"

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Android 10; Mobile; LG-M255; rv:88.0) Gecko/88.0 Firefox/88.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36",
    ]

    def __init__(self, max_pages=5):
        self.user_agent_position = 0
        self.agent = self.initiate_driver()
        self.page_count = 0
        self.max_pages = max_pages

    def initiate_driver(self) -> webdriver.Chrome:
        """
        Disabling the Automation Indicator WebDriver Flags
        https://www.zenrows.com/blog/selenium-avoid-bot-detection#disable-automation-indicator-webdriver-flags
        """
        options = webdriver.ChromeOptions()

        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled") 

        # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 

        # Turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome()

        # Changing the property of the navigator value for webdriver to undefined 
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

        return driver

    def rotate_user_agent(self) -> None:
        """
        Return a random user agent
        """
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {"userAgent": self.user_agents[self.user_agent_position]}
        ) 
        print("using", self.driver.execute_script("return navigator.userAgent;")) 
        self.user_agent_position = (self.user_agent_position + 1) % len(self.user_agents)

    def captcha_detected(self) -> bool:
        """
        Check if a captcha is detected
        """
        return False
    
    def sleep_randomly(self) -> None:
        """
        Sleep randomly
        """
        time.sleep(random.randint(1, 5))
    
    def save_data(self, data) -> None:
        """
        Save the data into the db
        """
        flat = Flat(
            title=data.get("title"),
            description=data.get("descrption"),
            price=data.get("price"),
            published_at=data.get("published_at"),
            address=data.get("address"),
            url=data.get("url"),
            source=self.name,
        )
        flat.save()

    def load_page(self, url: str) -> None:
        """
        Load the page
        """
        self.agent.get(url)
        self.sleep_randomly()

    def next_page(self) -> bool:
        if not self.page_count:  # first page
            self.load_page(self.base_url)
            return True
        
        if self.page_count >= self.max_pages:  # max pages reached
            return False

        self.sleep_randomly()
        next_page_link = self.driver.find_element_by_css_selector(self.next_page_selector)
        if next_page_link:
            next_page_link.click()
            self.page_count += 1
            return True
        return False
    
    def list_flats(self) -> list[Flat]:
        """
        Return a list of flats
        """
        return []