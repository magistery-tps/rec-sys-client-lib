# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación


Implementación de un sistema de recomendación punta a punta. Desde el scrapping de datos hasta la implementación de una aplicación y los algoritmos necesarios.

## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* [Setup de entorno (Window)](https://www.youtube.com/watch?v=O8YXuHNdIIk)
* mariadb/mysql


## Componentes

* **recsys**: Web app de recomendación de items. Permite recomendar items personalizados.
   * Login with google.
   * API: Permite administrar items, interacciones, users, matrices de distancia, etc.. via rest.
   * Pantalla para puntuación de items.
   * Pantalla de visialización de recommendaciones.
   * CRUD de items.
   * Admin site.

![RecSys Recommendations](https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot.png)

* **notebooks**
    * Pre-carga de datasets amazon sneakers o movie-lens.
        * **Amazon sneakers**: Datasets de zapatillas extraído de Amazon US.
            * [build-datasets](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/build-datasets.ipynb): Construcción de un datasets de items e interacciones de usuarios en base a files generados en la etapa de scrapping de datos.
            * [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/data-loader.ipynb): Carga de datos en la base de datos de **recsys** Abstraccion `Repository`.
        * **Movie Lens**: Datasets de películas con scoring personalizado.
            * [preprocessing](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/preprocessing.ipynb)
            * [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/data-loader.ipynb): Carga de datos en la base de datos de **recsys**.
    * [Administrar users, items, interacciones y matrices de distancia via api usando `RecSysApi`](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/api-client-test.ipynb)
    * Proceso para generacion de matrices de distancia en Airflow (Pending)


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
$ python manage.py runserver localhost:8000
```

**Step 7**: Ir a http://localhost:8000.

**Step 8**: Levantar jupiter lab.

```bash
$ jupyter lab

Jupyter Notebook 6.1.4 is running at:
http://localhost:8888/?token=45efe99607fa6......
```

**Step 9**: Ejecutar notebook [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/data-loader.ipynb): Carga de datos en la base de datos de **recsys** Abstraccion `Repository`.
