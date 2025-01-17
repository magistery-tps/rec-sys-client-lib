# recsys-client-lib

This library give support for:

* Access to [rec-sys](https://github.com/magistery-tps/rec-sys) via database repositories.
* Access to [rec-sys](https://github.com/magistery-tps/rec-sys) REST API to config and update recommenders data.
* Jobs: Used to build and config similarity matrix (user-user / item-item) required by [rec-sys](https://github.com/magistery-tps/rec-sys) recommenders.

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
from recsys.domain_context import DomainContext

ctx = DomainContext()
```

**Step 3**: Access to a _REST API_ client

```python
api_client = ctx.api

# Get user interactions
api_client.interacitons()
```
See [api.recsys.RecSysApi](https://magistery-tps.github.io/rec-sys-client-lib/api.html) for more detail.

**Step 3**: Execute a job.

```python
ctx.bert_item_distance_matrix_job('all-mpnet-base-v2').execute()

ctx.svd_distance_matrix_job.execute()

ctx.nmf_distance_matrix_job.execute()
```

See [job](https://magistery-tps.github.io/rec-sys-client-lib/job.html) for more detail.

**Step 4**: Also could run jobs from bash.

```bash
$ conda activate recsys-client-side

$ python bin/svd_distance_matrix_job.py

$ python bin/nmf_distance_matrix_job.py

$ python bin/all_minilm_l12_v2_bert_item_distance_matrix_job.py

$ python bin/all_mpnet_base_v2_bert_item_distance_matrix_job.py

$ python bin/all_minilm_l6_v2_bert_item_distance_matrix_job.py

$ python bin/multi_qa_mpnet_base_dot_v1_bert_item_distance_matrix_job.py
```

## API Documentation

Go to [rec-sys-client-side Documentation](https://magistery-tps.github.io/rec-sys-client-lib).

## WIKI

Go to [rec-sys WIKI](https://github.com/magistery-tps/rec-sys/wiki) for model project details.

