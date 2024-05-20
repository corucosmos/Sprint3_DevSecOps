# Sprint 2

## Descripción de la App

La App de este sprint es una aplicación que imprime en la consola "Hola Mundo" al hacer una petición GET al endpoint raíz de la aplicación.

El puerto por defecto en el que se ejecuta la aplicación es el 5000.

La información del puerto 5000 la toma promtail para enviársela a Loki en el puerto 3100.

### Endpoints expuestos desde la App

- GET /: Endpoint que imprime en la consola "Hola Mundo". Además, esta frase es la que se devuelve como respuesta a la petición en dicho endpoint
- GET /error: Endpoint que imprime en la consola "Error!". Además, esta frase es la que se devuelve como respuesta a la petición en dicho endpoint

### Resumen

Puedes acceder a la aplicación desde http://localhost:5000 si has ejecutado docker compose para arrancar la aplicación y servicios relacionados.