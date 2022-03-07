# Semana 5 - Despliegue de funciones como servicio

## Objetivos

- Aplicar los conocimientos y conceptos de aplicaciones serverless vistos en clase.
- Crear y publicar aplicaciones Cloud Function en GCP

## Estructura de carpetas

En el proyecto encontrará tres carpetas principales:

- La carpeta `collections` en donde se encuentra la colección de Postman para poder realizar pruebas sobre las funciones publicadas
- La carpeta `listar` en donde se encuentra la implementación de lafunción que nos da la lista completa de héroes 
- La carpeta `detalle` en donde se encuentra la implementación de lafunción que nos permite ver la información de un héroe especifico de acuerdo a un identificador  

## Publicacion de la funciones 

### Listar

Para poder publicar la función, debe abrir una consola de comandos en la ubicación donde descargamos el repositorio. Posteriormente, debe ejecutar los sigioentes comandos:

```console
cd listar
gcloud functions deploy funcion-heroes-listar --entry-point listar_heroes --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1
cd ..
```

En la consola deberá observar un mensaje de confirmación de creación de la función

### Detalle

Para poder publicar la función, debe abrir una consola de comandos en la ubicación donde descargamos el repositorio. Posteriormente, debe ejecutar los sigioentes comandos:

```console
cd detalle
gcloud functions deploy funcion-heroes-detalle --entry-point dar_heroe --runtime python39 --trigger-http --allow-unauthenticated --memory 128MB --region us-central1 --timeout 60 --min-instances 0 --max-instances 1
cd ..
```

En la consola deberá observar un mensaje de confirmación de creación de la función
