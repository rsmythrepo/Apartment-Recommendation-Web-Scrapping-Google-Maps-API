# Homie

This is a Python (+3.11) project with poetry to find the perfect place in any city of your preference.

By: Rogelio Martínez & Raphaelle Smyth

## How it works
1. Ingest the data from a CSV file or a scrapper
2. Run the Google Maps to find all services around
3. It will score and rank all places relevant base on your preferences.

## Settings
You need to create a .env file with the following vars
* `GOOGLE_MAPS_API_KEY`: TBD
* `GOOGLE_MAPS_DEFAULT_RADIUS`: TBD
* `SERVICES`: TBD

## Run
```sh
poetry run python menu.py
```

## Ingest the data
### CSV
Load a CSV file.

### Scrapper
List of scrappers and supported cities:
* TBD: TBD
* TBD: TBD



## Development
