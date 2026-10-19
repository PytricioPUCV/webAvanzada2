import pandas as pd
from scraper import obtener_libros


def main():
    libros = obtener_libros()
    df = pd.DataFrame(libros)

    print(df.head())
    df.info()
    print(df.shape)
    print(df.columns.tolist())

    df["titulo"] = (df["titulo"].fillna("").astype(str)
                    .str.strip().str.replace(r"\s+", " ", regex=True))
    df["disponibilidad"] = df["disponibilidad"].fillna("").astype(str).str.strip()
    df = df.drop_duplicates(subset="titulo").reset_index(drop=True)
    df["titulo_normalizado"] = df["titulo"].str.lower()

    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
    df["calificacion"] = pd.to_numeric(df["calificacion"], errors="coerce").astype("Int64")
    print("\nTipos tras la limpieza:")
    print(df.dtypes)

    print(f"\nCantidad de libros: {len(df)}")
    print(f"Precio promedio: {df['precio'].mean():.2f}")

    df.to_csv("libros.csv", index=False, encoding="utf-8")
    print("Archivo libros.csv generado.")


if __name__ == "__main__":
    main()