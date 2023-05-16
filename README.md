# PI-ML-HENRY-DS10

Data Engineering project to create a movies database.

This project consists of a raw dataset, which was cleaned with the Python library pandas,
the data of which is later served through an API using the FastAPI framework.
Using a Dockerfile, the API was deployed on Render to make it available for the
piblic to use.

There are 6 main functions in the API:
    - peliculas_mes: takes a month for an argument (in spanish), and returns the number
    of movies that were released hitorically in that month.
    - peliculas_dia: takes a weekday for an argument (in spanish), and returns the number
    of movies that were released hitorically in that weekday.
    - franquicia: takes the name of a franchise (collection), and returns how many
    movies the franchise has, along with the total and mean earnings the franchise has
    made so far.
    - peliculas_pais: takes a country name for an argument and returns how many movies
    that country has produced.
    - productoras: takes a production company name for an argument and returns the total
    earnings that producer has made and the amount of movies it has produced so far.
    - retorno: takes a movie name for an argument, and returns the investment cost,
    the earnings the movie produced, the net return of the movie and the year it was
    released.
