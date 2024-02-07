
# Selenium allows interaction with browser (buttons)

from .generics import Scrapper
from db.models import Flat


class IdealistaScrapper(Scrapper):
    base_url = "https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/"
    name = "idealista"

    def list_flats(self) -> list:
        """
        Return a list of flats
        """
        flats = []
        items = self.driver.find_elements_by_css_selector(".item-info-container")
        for item in items:
            flat = Flat(
                title=item.find_element_by_css_selector(".item-link").text,
                url=item.find_element_by_css_selector(".item-link").get_attribute("href"),
                price=self.clean_price(item.find_element_by_css_selector(".item-price").text),
                space=self.clean_space(item.find_element_by_css_selector(".item-detail").text),
                source=self.name,
            )
            flats.append(flat)
        return flats

    def flat_details(self, flat: Flat) -> Flat:
        """
        Get the details of a flat
        """
        self.load_page(flat.url)
        flat.published_at = self.driver.find_element_by_css_selector(".info-data").text
        flat.address = self.driver.find_element_by_css_selector(".main-info").text
        return flat

    def clean_price(self, price:str):
        return float(price.split("€")[0])
    
    def clean_space(self, space:str):
        return int(space.split(" ")[0])
