# PT API

## Run locally

Python version: 3.11
This project uses Poetry for managing dependencies.
To run service locally install all required packages:

`poetry install`

And then run the main file:

`poetry run python src/main.py`

### Formatting

`poetry run black src`

### Tests

To trigger tests run:

`poetry run pytest`

## Future improvements
### Business
- Add Rolygon query param: allows to retrieve data based on a provided list of coordinates that form a closed shape(polygon)
- Cover more data with query params, including nested
- Add sorting
- Add Return Fields query param: allows to name fields the user want to see in response

### Engineering
- Replace static file with DB, e.g. Postgres or PostGIS
- Add caching
- Introduce a lib to work with geo spacial data, e.g. `geopandas`
- Increace test coverage, add integration tests
- Add more validation for edge cases
- Add Error handling
- Flatten response
