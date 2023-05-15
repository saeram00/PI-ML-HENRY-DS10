import pandas as pd
from fastapi import FastAPI

from pathlib import Path

mes_es = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

dias_semana_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

DATA_SOURCE = Path(__file__).parent.joinpath(
    "data",
    "cleaned_dataset.csv"
).resolve()
app = FastAPI(title="DB Peliculas")

df = pd.read_csv(DATA_SOURCE, low_memory=False)

# Traducir dias de la semana y meses de inglés a español y agregarlos
# como nuevas columnas al DataFrame
df["release_date"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d")
df["release_month"] = df["release_date"].apply(
    lambda x: mes_es[x.strftime("%B")]
)
df["release_weekday"] = df["release_date"].apply(
    lambda x: dias_semana_es[x.strftime("%A")]
)

@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str) -> dict:
    """
    Se ingresa el mes y la funcion retorna la cantidad de peliculas
    que se estrenaron ese mes historicamente.

    :param mes: El mes del cual se busca conocer la cantidad.

    :returns: Un diccionario que contiene el mes ingresado y la
    cantidad de películas estrenadas en ese período.
    """

    df_mes = df[df["release_month"] == mes.capitalize()]
    cantidad = df_mes.shape[0]
    return {
        "mes": mes,
        "cantidad": cantidad
    }


@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia: str) -> dict:
    """
    Se ingresa el dia y la funcion retorna la cantidad de peliculas
    que se estrenaron ese dia historicamente.

    :param dia: El día de la semana del cual se busca conocer
    la cantidad.

    :returns: Un diccionario que contiene el día ingresado y la
    cantidad de películas estrenadas tal día históricamente.
    """

    df_dia = df[df["release_weekday"] == dia.capitalize()]
    cantidad = df_dia.shape[0]
    return {
        "dia": dia,
        "cantidad": cantidad
    }


@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str) -> dict:
    """
    Se ingresa la franquicia, retornando la cantidad de peliculas,
    ganancia total y promedio.

    :param franquicia: Nombre de la franquicia de la cual se
    quiere realizar la consulta.

    :returns: Un diccionario que contiene la franquicia ingresada,
    la cantidad de películas que existen dentro de ésta, las ganancias
    totales de dicha franquicia y las ganancias promedio de la misma.
    """

    franquicia_df = df[df["name_collection"].apply(
        lambda x: x is not None and x["name"] == franquicia
    )]
    cantidad = len(franquicia_df)
    ganancia_total = franquicia_df["revenue"].sum()
    ganancia_promedio = franquicia_df["revenue"].mean() if cantidad > 0 else 0
    return {
        "franquicia": franquicia,
        "cantidad": cantidad,
        "ganancia_total": ganancia_total,
        "ganancia_promedio": ganancia_promedio
    }


@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str) -> dict:
    """
    Ingresas el pais, retornando la cantidad de peliculas producidas
    en el mismo.

    :param pais: El país del cual se quiera saber la cantidad.

    :returns: Un diccionario que ccontiene el país ingresado y
    la cantidad de películas producidas por éste.
    """

    pais_df = df[df["production_countries"].apply(
        lambda x: any(d["name"] == pais for d in x)
    )]
    cantidad = len(pais_df)
    return {
        "pais": pais,
        "cantidad": cantidad
    }


@app.get("/productoras/{productora}")
def productoras(productora: str) -> dict:
    """
    Ingresas la productora, retornando la ganancia total y
    la cantidad de peliculas que produjeron.

    :param productora: El nombre de la productora de la cual
    se quiere saber su información.

    :returns: Un diccionario que contiene el nombre de la productora
    ingresada, las ganancias totales de dicha productora y la
    cantidad de películas producidas por ésta.
    """

    productora_df = df[df["production_companies"].apply(
        lambda x: any(d["name"] == productora for d in x)
    )]
    ganancia_total = productora_df["revenue"].sum()
    cantidad = productora_df["revenue"].count()
    return {
        "productora": productora,
        "ganancia_total": ganancia_total,
        "cantidad": cantidad
    }


@app.get("/retorno/{pelicula}")
def retorno(pelicula: str) -> dict:
    """
    Ingresas la pelicula, retornando la inversion, la ganancia,
    el retorno y el año en el que se lanzo.

    :param pelicula: El nombre de la película de la cual se quiere
    saber su información.

    :returns: Un diccionario que contiene el nombre de la película
    ingresada, el monto de inversión de su producción, el monto
    de la ganancia total generada por dicha película, el valor
    de retorno producido por la misma y el año en que fue estrenada.
    """

    pelicula_df = df.loc[df["title"] == pelicula.title()]
    inversion = pelicula_df["budget"].iloc[0].item()
    ganancia = pelicula_df["revenue"].iloc[0].item()
    retorno = pelicula_df["return"].iloc[0].item()
    anio = pelicula_df["release_year"].iloc[0].item()
    return {
        "pelicula": pelicula,
        "inversion": inversion,
        "ganacia": ganancia,
        "retorno": retorno,
        "anio": anio
    }
