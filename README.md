# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación


## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* [Setup de entorno (Window)](https://www.youtube.com/watch?v=O8YXuHNdIIk)
* mariadb/mysql


## Componentes

* **recsys**: Web app de recomendación de items. Permite recomendar items personalizados.
 * Login with google
 * Api: Permote administrar itmes, interacciones y matrices de distancia via rest.
 * Pantalla de punciacion de items.
 * Pantalla de visializacionde recommendaciones.
 * Cdud de items.

![RecSys Recommendations](https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot.png)

* **Notebooks**
    * Pre-carga de datasets amazon sneakers o movie-lens.
        * **Amazon sneakers**: Datasets de zapatillas extraído de Amazon US.
            * [build-datasets](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/build-datasets.ipynb): Construcción de un datasets de items e interacciones de usuarios en base a files generados en la etapa de scrapping de datos.
            * [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/data-loader.ipynb): Carga de datos en la base de datos de **recsys**.
        * **Movie Lens**: Datasets de películas con scoring personalizado.
            * [preprocessing](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/preprocessing.ipynb)
            * [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/data-loader.ipynb): Carga de datos en la base de datos de **recsys**.

* **[amazon-spider-scrapper](https://github.com/adrianmarino/amazon-spider-scrapper)**
    * Es un fork del proyecto amazon-scrapper.
    * Dada una búsqueda en Amazon, permite realizar scrapping del detalle de todos los resultados (Productos) y sus variaciones, junto con sus reviews.
    * Utiliza headers fake, proxies random y delays variables para minimizar el banning de Amazon.
    * Permite, reanudar el proceso de scrapping desde el ultimo productos scrappeado.

## Comenzando

**Step 1**: Clonar repo.

```bash
$ git clone https://github.com/adrianmarino/rec-sys.git
$ cd rec-sys
```

**Step 2**: Crear environment.

```bash
$ conda env create -f environment.yml
```

**Step 3**: Activar environment.

```bash
$ conda activate rec-sys
```

**Step 4**: Create database.

```bash
$ mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS recsys"
$ python manage.py migrate
```

**Step 5**: Create admin user.

```bash
$ python manage.py createsuperuser
```

**Step 6**: Boot web application.

```bash
$ cd recsys
$ python manage.py runserver
```

**Step 7**: Ir a http://127.0.0.1:8000.

