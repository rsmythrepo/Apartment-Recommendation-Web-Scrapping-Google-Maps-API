
# Selenium allows interaction with browser (buttons)

from .generics import Scrapper


class Idealista(Scrapper):
    """
    Data about the webpage:
    - country:
    - cities:
    """
    base_url = "[TODO]"
    name = "idealista"

    def get_data(self) -> dict:
        pass