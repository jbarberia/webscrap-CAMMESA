# webscrap-CAMMESA
Este paquete fue creado para la extracción de los datos historicos por hora de los diferentes tipos de energias renovables de la pagina web de CAMMESA. A su vez tambien puede extraer los datos historicos por hora de diferentes estaciones meteorologicas de acuerdo a los registros del SMN.

## Uso
Para su uso se deben usar los metodos `.download_by_date(date: datetime.date)`.

```python
scraper = CAMMESAScraper()
fecha = date.fromisoformat("2021-12-10")
scraper.download_by_date(fecha)
```

Los nombres de los archivos que se descargan para el dia `2021-12-10` son:

| Fuente  | Nombre de archivo             | Ubicación           |
|---------|-------------------------------|---------------------|
| CAMMESA | EvoluciónTemporal_10122021.csv| `C:\Users\Downloads`|
| SMN     | datohorario20211210.txt       | Especificada        |

Luego de descargar los archivos, los cuales solamente los datos del SMN se pueden redireccionar a una nueva carpeta. Se podra procesar la información uniendo las correspondientes bases de datos.

> **Advertencia**:
> La union de las bases de datos se realiza con el metodo `outer`, lo cual es posible una gran perdida de datos en el proceso de union de las bases de datos.
