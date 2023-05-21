# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación - recsys-client-side API

This repository give support to:

* Access to [rec-sys](https://github.com/magistery-tps/rec-sys) via database repositories.
* Acces to [rec-sys](https://github.com/magistery-tps/rec-sys) REST API to config and update recommender data.
* Jobs: Used to build ad config similarities matrix (user-user / item-item) required by [rec-sys](https://github.com/magistery-tps/rec-sys) recommenders.

## Requirements

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recommended)](https://github.com/mamba-org/mamba)
* mariadb/mysql


## Getting Started

**Step 1**: First Import `src` directory into python class path:

```python
import sys
sys.path.append('./src')
```

**Step 2**: Import `DomainContext` class. `DomainContext` is a python class that build and config all services required to interact with [rec-sys](https://github.com/magistery-tps/rec-sys) via _REST API_ or _Database Client_. `DomainContext` can be seen as a `facade` pattern. 

```python
from domain_context import DomainContext

ctx = DomainContext()
```

**Step 3**: Access to a _REST API_ client

```python
api_client = ctx.api

# Get user interactions
api_client.interacitons()
```
See [api.recsys.RecSysApi](https://magistery-tps.github.io/rec-sys-client-side/#api-package) for more detail.

**Step 3**: Execute a job.

```python
DomainContext().bert_item_distance_matrix_job('all-mpnet-base-v2').execute()

DomainContext().svd_distance_matrix_job.execute()

DomainContext().nmf_distance_matrix_job.execute()
```

See [jons.Job](https://magistery-tps.github.io/rec-sys-client-side/#jobs-package) for more detail.


## API Documentation

Got to [rec-sys-client-side Documentation](https://magistery-tps.github.io/rec-sys-client-side).

## WIKI

Go to [rec-sys WIKI](https://github.com/magistery-tps/rec-sys/wiki) for model project details.

