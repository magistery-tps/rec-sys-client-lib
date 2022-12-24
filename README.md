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

<p align="center">
<img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_2.png"  height="550" />
</p>


* **notebooks**
    * Pre-carga de datasets amazon sneakers o movie-lens.

       * **[Amazon Books](https://nijianmo.github.io/amazon/index.html)**: Datasets de zapatillas extraído de Amazon US.
   
            * **[build-datasets](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-books/build-datasets.ipynb)**
              * Preprocesamiento.
              * Seleccion de features.
              * Construcción de un datasets de items e interacciones de usuarios.
            * **[data-loading](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-books/data-loader.ipynb)**
              *  Preprosesamiento final.
              *  Filtro de item e interaciones segun un minimo de popilaridad
              *  Carga de datos via SQL en  `RecSysApi`.
            * **[similarity-matrix-jobs](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-books/distance-matrix-job.ipynb)**
              * Prueba de escritorio de los siguientes jobs:
                * _svd_distance_matrix_job_
                * _nmf_distance_matrix_job_
              * Ambos jobs son instancias de _SurpriseDistanceMatrixJob_.
              * _SurpriseDistanceMatrixJob_ consulta las interacciones via REST a  `RecSysApi`.
              * Predice los ratings de las interacciones faltantes.
              * Cosntruye una matrix de ratings completa. Es decir, esta contien las interacciones actuales y las predichas.
              * Calcula las similitudes user-user/item-item, solo para un numero N de usuarios e items vecinos. Esto disminuir los tiempo de ejecución y evita tener en tienta usuario e item muy lejanos.
              * Finalmente, crear o actualiza via REST (En  `RecSysApi`) las entidades _Recommender_ para cada modelos SVD y NMF, junto con sus propias matrices de similitud (_SimilarityMatrix_, entidades asociada a _Recommender_).
              * Las entidades _SimilarityMatrix_ son versionadas cada vez que correr cada job. Al correr un job, se crea una nueva versión de las matrices. Al finalizar el proceso, se borra la versión anterior quendado disponibilizada la nueva versión. Es posible mantener una ventana de versiones, pero por el momento no es necesario.
              * Los jobs solo se ejecutan cuando se encuentran nuevas interacciones, para evitar re-procesamiento innecesario.
       
       * **[Amazon Sneakers](https://www.amazon.com/sneakers/s?k=sneakers)**: Datasets de zapatillas extraído de Amazon US.
            * **[build-datasets](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-sneakers/build-datasets.ipynb):** Construcción de un datasets de items e interacciones de usuarios en base a files generados en la etapa de scrapping de datos.
            * **[data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon-sneakers/data-loader.ipynb):** Carga de datos en la base de datos de **recsys** Abstraccion `Repository`.
       
       * **[Movie Lens](https://grouplens.org/datasets/movielens/)**: Datasets de películas con scoring personalizado.
            * **[preprocessing](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/preprocessing.ipynb)**
            * **[data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/movielens/data-loader.ipynb):** Carga de datos en la base de datos de **recsys**.
    * **[`RecSysApi` client testing](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/api-client-test.ipynb):** Administrar users, items, interacciones y matrices de distancia via api usando `RecSysApi`.
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

**Step 4**: Crear base de datos.

```bash
$ mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS recsys"
$ python manage.py migrate
```

**Step 5**: Cear usuario administrador.

```bash
$ python manage.py createsuperuser
```

**Step 6**: Iniciar aplicación web utilizando una clave secreta dummy.

```bash
$ cd recsys
$ export SECRET_KEY="^BJ>Nzq>*8[HKH/ew:]TdfgD<nul;v9R571yvxI"
$ python manage.py runserver localhost:8000
```

**Step 7**: Ir a http://localhost:8000.

**Step 8**: Levantar jupiter lab.

```bash
$ cd ../
$ jupyter lab

Jupyter Notebook 6.1.4 is running at:
http://localhost:8888/?token=45efe99607fa6......
```

**Step 9**: Ejecutar notebook [data-loader](https://github.com/magistery-tps/rec-sys/blob/main/notebooks/amazon/data-loader.ipynb): Carga de datos en la base de datos de **recsys** Abstraccion `Repository`.



## Calcular Matrices de Similitud

**Step 1**: Activar environment.

```bash
$ conda activate rec-sys
```

**Step 2**: Calcular matrices de distancia utilizando SVD.

```bash
$ cd recsys
$  python bin/svd_distance_matrix_job.py
```

**Step 3**: Calcular matrices de distancia utilizando NMF.

```bash
$ cd recsys
$  python bin/nmf_distance_matrix_job.py
```

Ambos jobs calcular matrices de distancia user-user/item-item en base a la matriz de rating predicha por cada model (SVD/NMF). Luego, realizan un upsert de estas matrices en la base de datos, insertando unicamente los N vecinos mas cercanos en ambos casos (user-user/item-item). Cada matrix esta versionada. Es decir, que cada ejecución de un job crear una nueva versión de la matrix. Finalmente, ambas matrices queda asociadas a una entidad en la base de datos que representa al modelo con el que fue predicha.



## Correr aplicación como un servicio/demonio systemd


**Step 1**: Clonar repo.

```bash
$ cd ~
$ git clone https://github.com/adrianmarino/airflow-systemd.git
$ mv airflow-systemd airflow
$ cd recsys
```

**Step 2**: Crear conda environment requerido para correr recsys como un servicio.

```bash
$ conda env update -f environment.yml
```

**Step 3**: Copiar file.service a `~/.config/systemd/user/`:

```bash
$ cp recsys.service ~/.config/systemd/user/
```

**Step 4**: Importar variable de entoeno requeridas por la aplicación:

```bash
$ echo "source ~/recsys/.shell.recsysrc" >> ~/.bashrc
ó
$ echo "source ~/recsys/.shell.recsysrc" >> ~/.zshrc
```


**Step 4**: Referscar la configuración de systemd.

```bash
$ systemctl --user daemon-reload
```

**Step 5**: Habilitar el servicio apra que se inie al bootear el sistema.

```bash
$ systemctl --user enable recsys
```

**Step 6**: Iniciar el servicio en background.

```bash
$ systemctl --user start recsys
```
