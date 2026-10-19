# Laboratorio 2 - Web Scraping y buscador de títulos

Integrantes: Patricio Hernández, Ignacio Reyes
Repositorio: https://github.com/PytricioPUCV/webAvanzada2

## Entorno virtual

py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

## Orden de ejecución

```
python scraper.py
python procesamiento.py
python buscador.py
```

Si a un libro le falta un dato, queda como None. Si un libro falla, se muestra un aviso y se sigue con el siguiente.

## Resultados

- Libros extraídos: 20
- Precio promedio: 38.05

Búsqueda "life":
```
Scott Pilgrim's Precious Little Life (Scott Pilgrim #1) | Precio: 52.29 | Similitud: 0.2459
The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull | Precio: 17.93 | Similitud: 0.2250
Our Band Could Be Your Life: Scenes from the American Indie Underground, 1981-1991 | Precio: 57.25 | Similitud: 0.2231
```

Búsqueda "light":
```
A Light in the Attic | Precio: 51.77 | Similitud: 0.5760
```

Con "life" salen 3 libros y el primero es el de título más corto, porque ahí la palabra pesa más. Con "light" sale solo uno, con más puntaje, porque es el único título que la tiene.

Con top_k=3 y la consulta "the" salieron solo 3 resultados.

## Pruebas

| Caso | Consulta | Resultado | Estado |
|---|---|---|---|
| T1 | life | 3 resultados ordenados de mayor a menor similitud | Cumple |
| T2 | zzxyz123 | "No se encontraron coincidencias." | Cumple |
| T3 | LIFE | Mismo ranking que T1 | Cumple |
| T4 | (vacía) | "Ingrese una consulta no vacia." y "No se encontraron coincidencias.", sin error | Cumple |

## Respuestas

1. requests solo descarga el HTML de la página como texto. BeautifulSoup lo parsea para poder buscar elementos con selectores y sacar los datos.

2. Si el sitio cambia sus clases o su estructura, los selectores dejan de funcionar y el scraper puede fallar o sacar datos incompletos sin avisar.

3. Para reducir variaciones como las mayúsculas, así "Life" y "life" cuentan como la misma palabra.

4. fit_transform() aprende el vocabulario de los títulos y crea la matriz TF-IDF. Con la consulta se usa transform() para que quede con el mismo vocabulario y se pueda comparar.

5. Primero sale el de 0.75, porque se ordena de mayor a menor. Un puntaje cerca de cero significa que el título casi no comparte palabras con la consulta.

6. TF-IDF solo encuentra palabras exactas y no entiende el significado, entonces no encuentra sinónimos ni palabras en otro idioma. Una mejora sería usar búsqueda semántica con embeddings o combinarla con TF-IDF (búsqueda híbrida).