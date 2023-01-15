# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación


Implementación de un sistema de recomendación punta a punta. Desde el scrapping de datos hasta la implementación de una aplicación y los algoritmos necesarios.

## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* [Setup de entorno (Window)](https://www.youtube.com/watch?v=O8YXuHNdIIk)
* mariadb/mysql

## Screenshots


### Recomendaciones
![See Recommendations](https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot.png)

**Notas**
* Al hacer click sobre un item, se puede visualizar el detalle del mismo junto con sus items similares.

### Item Detail & Similars

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_3.png"  height="550" />
</p>

**Notas**
* Al hacer click sobre los simialres se abre su detalle junto con sus simialres.
* Los item similares dependen del recomendador seleccionado en la vista de recommendaciones.
* Ademas de las estadisticas asociadas a cada item es posible ver las similitud coseno de cada item similar al item detallado.
* Los items similares estan ordenados por similitud coseno decreciente.

### Scoring

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_2.png"  height="295" />
</p>

**Notas**
1. Selecionar scoring o rating para el item actual.
2. Presione **Vote** para aplicar el score selecionado en el punto 1 al item actual.
3. Presione **Next** para saltear la votation del item actuar.
4. El valor de estadisticas como popularidad, rating y cantidad de votaciones del item actual.
5. Al hacer click sobre la imagen, es posible ver el detalle del item.


## [WIKI](https://github.com/magistery-tps/rec-sys/wiki)

Para mas detalle de como instalar la aplicación y detalla de implementación ver la [WIKI](https://github.com/magistery-tps/rec-sys/wiki) del proyecto.
