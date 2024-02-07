from db.models import Flat

from .idealista import IdealistaScrapper

if __name__ == "__main__":
    scrapper = IdealistaScrapper()
    scrapper.load_page("https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/")

    # general data
    flats = []
    while scrapper.next_page():
        flats = scrapper.list_flats()  # only general data
        Flat.save_multiple(flats)

    # detailed data
    for flat in flats:
        flat = scrapper.flat_details(flat)
        flat.save()
