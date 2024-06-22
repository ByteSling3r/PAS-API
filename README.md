# Pas-API

## Descripción
Este API en Flask proporciona una interfaz para gestionar Dispositivos IOT en especifico Luces y Ventilador. Esta API está diseñada para el Proyecto de Aula Semestral (PAS)

## Instalación
1. Clona el repositorio: `git clone https://github.com/ByteSling3r/PAS-API.git`
2. Navega hasta la carpeta del proyecto: `cd PAS-API`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Configura la base de datos: `flask db migrate && flask db upgrade`
5. Inicia el servidor: `python run.py`

## Endpoints
- `/api/state`: Devuelve el stado de los dispositivos conectados y envio de actualización del estado.
- `/api/activities`: Devuelve el registro del dia y de las veces que se manipuló los dispositivos conectaddos.
- `/api/progamming`: Agrega la programación de encendido/apagado de los dispositivos conectados.

## Uso
Para utilizar este API, realiza las siguientes solicitudes HTTP:

- GET `/api/state`: Obtiene el estado de los dispositivos conectados(Luces y Ventilador).
- PUT `/api/state`: Edita los valores de ON y OFF en los dispostivos conectados.
- GET `/api/activities`: Obtiene el registro del dia y de las veces que se manipuló los dispositivos conectaddos.
- POST `/api/programming`: Agrega la programación de la hora de encendido y apagado.

## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto [correo electrónico de contacto](mailto:juanddelgadoguerra@gmail.com).
