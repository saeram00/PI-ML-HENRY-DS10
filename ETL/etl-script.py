import pandas as pd

import sys
from pathlib import Path


DATA_DIR = Path(__file__).parents[1].joinpath("data").resolve()
DATA_SOURCE = DATA_DIR.joinpath("movies_dataset.csv").resolve()

def main():
    df = pd.read_csv(DATA_SOURCE, low_memory=False)

    # Eliminar columnas innecesarias
    df.drop(
        columns=[
            "adult",
            "imdb_id",
            "homepage",
            "original_title",
            "poster_path",
            "video",
            "vote_count"
        ],
        inplace=True
    )

    # Rellenar valores faltantes en columnas "revenue" y "budget" con 0
    df.fillna(
        value={
            "revenue": 0,
            "budget": 0
        },
        inplace=True
    )

    # Eliminar valores faltantes de columna "release_date"
    df.dropna(subset=["release_date"], inplace=True)

    # Convertir columna "release_date" a datetime, y crear columna
    # "release_year" en base al año de "release_date"
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year.astype(pd.Int16Dtype())

    # Eliminar registros no válidos
    df.drop(
        index=df[df["budget"].str.isdigit() == False].index,
        inplace=True
    )

    # Convertir columna "budget" de string a float, y obtener columna
    # "return" en base a "revenue" / "budget". De no ser posible hacer tal
    # cálculo, evalúa a 0
    df["budget"] = df["budget"].astype(pd.Float64Dtype())
    df["return"] = df.apply(
        lambda row: row["revenue"] / row["budget"] if (
            pd.notnull(row["revenue"])
            and pd.notnull(row["budget"])
            and row["budget"] != 0
        ) else 0,
        axis=1
    )

    # Convertir DataFrame limpio a archivo CSV
    df.to_csv(DATA_DIR.joinpath("cleaned_dataset.csv"), sep=",", index=False)


if __name__ == "__main__":
    rc: int = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    finally:
        sys.exit(rc)