# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación - client side applications

Este repositorio contiene soporte para implementar:

* Acceso via repositorios a base de datos de [rec-sys](https://github.com/magistery-tps/rec-sys).
* Acceso via api REST para configurar recomendadores y actualizar datos en [rec-sys](https://github.com/magistery-tps/rec-sys).
* Jobs: Construccion y actaializacion de matrices de similitud user-user e item-item en [rec-sys](https://github.com/magistery-tps/rec-sys) utilizando los modelos SVD, NFM y Bert.

## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* mariadb/mysql


## Uso

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

**Step 3**: Acces to a _REST API_ client

```python

api_client = ctx.api




```


#------------------------------------------------------------------------------
#
#
#
#
#------------------------------------------------------------------------------
# Main
#------------------------------------------------------------------------------
if __name__ == '__main__':
    DomainContext().bert_item_distance_matrix_job('all-mpnet-base-v2').execute()
#------------------------------------------------------------------------------


```


## WIKI

Para mas detalle ver la [WIKI](https://github.com/magistery-tps/rec-sys/wiki) del proyecto.

