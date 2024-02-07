# Homie
This is a Python (+3.11) with poetry.

## Install
```sh
poetry install
```

Add new depedencies:
```sh
poetry add {dependency}
```

## Run
```sh
poetry run python your-script.py
```

### Ennviroment variables
Create a file `.env` in the root of the project
See also: `homie.settings.py`

These are the expected vars:
* GOOGLE_MAPS_API_KEY
* GOOGLE_MAPS_DEFAULT_RADIUS


## Linting
```sh
poetry run ruff --fix
```

## Database
SQLite is used with SQLModel using Pydantic and SQLAlchemy

## Gatering data

### Google Maps API
* Google API https://mapsplatform.google.com/
  * Pricing: https://mapsplatform.google.com/pricing/

### Scrappers
* idealista (url)
* [TODO]

### CSV

## Tests
[TODO]