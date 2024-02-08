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


## Linting
```sh
poetry run ruff --fix
```

## Database
SQLite is used with SQLModel using Pydantic and SQLAlchemy

## Gatering data

### Database
*Create or update an object*
```python
from db.session import db_session

@db_session  # will create/close a session and inject it into the function
def create_flat(session):
    flat = Flat(
      name="Amazing Flat in Barcelona",
      postalcode="08135",
      ...
    )
    session.add(flat)  # if flat.id is None will crete a new flat and assign an id automatically
    session.commit()
```


*Save multiple objects*
```python
from db.session import db_session

@db_session  # will create/close a session and inject it into the function
def get_flats(session, flats: list[Flat]):
    # SQLModel (Flat) objects are necessary to save data into the db
    for flat in flats:
        session.add(flat)
    
    session.commit()  # commit to save all flats added to the sessions
```


### Google Maps API
* Google API https://mapsplatform.google.com/
  * Pricing: https://mapsplatform.google.com/pricing/

### Scrappers
* idealista (url)
* [TODO]

### CSV
* CSV load supported
* All items must be separeted by a comma ","
* All datetime value must be str in ISO-datetime format

## Tests
[TODO]