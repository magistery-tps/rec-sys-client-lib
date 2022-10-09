# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendation


## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* [Setup de entorno (Window)](https://www.youtube.com/watch?v=O8YXuHNdIIk)
* mariadb/mysql

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

