# UBA - Maestría en Explotación de Datos y Descubrimiento de Conocimiento - Sistemas de recomendación


Implementación de un sistema de recomendación end-to-end. Desde el scrapping de datos hasta la implementación de una aplicación y los algoritmos necesarios.

## Requisitos

* [anaconda](https://www.anaconda.com/products/individual) / [miniconda](https://docs.conda.io/en/latest/miniconda.html) / [mamba (Recomendado)](https://github.com/mamba-org/mamba)
* [Setup de entorno (Window)](https://www.youtube.com/watch?v=O8YXuHNdIIk)
* mariadb/mysql

## WIKI

Para mas detalle ver la [WIKI](https://github.com/magistery-tps/rec-sys/wiki) del proyecto.


## Probar RecSys

Ir a  [recsys.sytes.net](http://recsys.sytes.net)

## Screenshots

### Recomendaciones
![See Recommendations](https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot.png)

**Notas**
* 1,2 y 3 con resultados de 3 distintos recomendadores. Es posible configurar ditintos recomendadores y ensambles de los mismo.
* Al hacer click sobre un ítem, se puede visualizar el detalle del mismo junto con sus items similares.
* Los distintos carruseles o swimlanes de recomendaciones representan a distintos recomendadores.
* Inicialmente se pueden ver los recomendadores por defecto:
   * Top populars.
   * New Populars: Populares no vistos por el usuario.
* Dependiendo de los recomendadores o ensambles de recomendadores que se configuren, es necesario cumplir con un número mínimo de calificaciones para comenzar a visualizar sus recomendaciones. Por ejemplo, para recomendadores basados en filtros colaborativos, se requiere que el usuario califique 20 ítems como mínimo. Los ensambles de recomendadores combinan recomendadores basados en filtros colaborativos con recomendadores por popularidad o basados en contenido. Los ensambles pueden no tener un requisito mínimo de calificaciones, depende de la configuración.


### Item Detail & Similars

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_2.png"  height="550" />
</p>

**Notas**
* Al hacer click sobre los simialres se abre su detalle junto con sus simialres.
* Los item similares dependen del recomendador seleccionado en la vista de recommendaciones.
* Ademas de las estadisticas asociadas a cada item es posible ver las similitud coseno de cada item similar al item detallado.
* Los items similares estan ordenados por similitud coseno decreciente.

### Scoring

<p align="center">
  <img src="https://github.com/magistery-tps/rec-sys/blob/main/images/screenshot_3.png"  height="295" />
</p>

**Notas**
1. Selecionar scoring o rating para el item actual.
2. Presione **Vote** para aplicar el score selecionado en el punto 1 al item actual.
3. Presione **Next** para saltear la votation del item actuar.
4. El valor de estadisticas como popularidad, rating y cantidad de votaciones del item actual.
5. Al hacer click sobre la imagen, es posible ver el detalle del item.

