import re
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
ESTRELLAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def convertir_precio(texto):
    limpio = re.sub(r"[^\d.]", "", texto or "")
    try:
        return float(limpio)
    except ValueError:
        return None


def convertir_calificacion(etiqueta):
    if etiqueta is None:
        return None
    for clase in etiqueta.get("class", []):
        if clase in ESTRELLAS:
            return ESTRELLAS[clase]
    return None


def obtener_libros(url=URL):
    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()
    respuesta.encoding = "utf-8"
    soup = BeautifulSoup(respuesta.text, "html.parser")

    libros = []
    for articulo in soup.select("article.product_pod"):
        try:
            enlace = articulo.select_one("h3 a")
            precio = articulo.select_one("p.price_color")
            disponibilidad = articulo.select_one("p.availability")
            estrellas = articulo.select_one("p.star-rating")

            titulo = enlace.get("title", "").strip() if enlace else ""

            libros.append({
                "titulo": titulo or None,
                "precio": convertir_precio(precio.get_text(strip=True) if precio else ""),
                "disponibilidad": disponibilidad.get_text(strip=True) if disponibilidad else None,
                "calificacion": convertir_calificacion(estrellas),
            })
        except Exception as error:
            print(f"Aviso: se omitió un libro por un error de extracción: {error}")
            continue
    return libros


if __name__ == "__main__":
    libros = obtener_libros()
    print(f"Total de libros extraídos: {len(libros)}")
    for libro in libros[:5]:
        print(libro)