# Microservicio de Usuarios

Este microservicio es responsable de gestionar los usuarios dentro de la aplicación, proporcionando funcionalidades clave para la creación, actualización, autenticación y consulta de datos de usuario.

## Índice

- [Microservicio de Usuarios](#microservicio-de-usuarios)
  - [Índice](#índice)
  - [Estructura](#estructura)
  - [Ejecución](#ejecución)
  - [Uso](#uso)
    - [Endpoints Disponibles](#endpoints-disponibles)
  - [Uso](#uso-1)
    - [1. Creación de usuarios](#1-creación-de-usuarios)
    - [2. Actualización de usuarios](#2-actualización-de-usuarios)
    - [3. Webhook de verificación de usuario](#3-Webhook-de-verificación-de-usuario)
    - [4. Generación de token](#4-generación-de-token)
    - [5. Consultar información del usuario](#5-consultar-información-del-usuario)
    - [6. Consulta de salud del servicio](#6-consulta-de-salud-del-servicio)
    - [7. Restablecer base de datos](#7-restablecer-base-de-datos)
  - [Pruebas](#pruebas)
    - [Requisitos previos](#requisitos-previos)
    - [Comandos para ejecutar las pruebas](#comandos-para-ejecutar-las-pruebas)
  - [Otras Características (opcional)](#otras-características-opcional)
  - [Autor](#autor)

## Estructura

La estructura de archivos del microservicio es la siguiente:

```
token-flask/
├── .github/                      # Pipelines de la aplicación
├── user/                         # Directorio del microservicio de usuarios (user)
│   ├── src/                      # Código fuente del microservicio
│   │   ├── blueprints/           # Contiene los blueprints de la aplicación Flask
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── commands/             # Lógica de negocio organizada por comandos
│   │   │   ├── __init__.py
│   │   │   ├── base_command.py
│   │   │   ├── create_user.py
│   │   │   ├── generate_token.py
│   │   │   ├── get_user_info.py
│   │   │   ├── reset_database.py
│   │   │   └── update_user.py
│   │   ├── errors/               # Manejo de errores personalizados
│   │   │   ├── __init__.py
│   │   │   └── errors.py
│   │   ├── models/               # Modelos y esquemas de datos de usuario
│   │   │   ├── __init__.py
│   │   │   ├── base_model.py
│   │   │   ├── model.py
│   │   │   ├── schemas.py
│   │   ├── database.py           # Base de datos
│   │   └── main.py               # Punto de entrada de la aplicación
│   ├── tests/                    # Pruebas unitarias para el microservicio
│   │   ├── blueprints/           # Pruebas para los blueprints
│   │   │   └── test_user.py
│   │   ├── commands/             # Pruebas para los comandos
│   │   │   ├── test_create_user.py
│   │   │   ├── test_generate_token.py
│   │   │   ├── test_get_user_info.py
│   │   │   ├── test_reset_database.py
│   │   │   └── test_update_user.py
│   │   └── conftest.py           # Archivo de configuración para pytest
│   ├── Dockerfile                # Definición de la imagen Docker
│   ├── Pipfile                   # Dependencias del proyecto
│   ├── Pipfile.lock              # Versiones bloqueadas de dependencias
│   └── README.md                 # Documentación del microservicio
├── config.yaml                   # Archivo de configuraciones de despliegue de ejecución de microservicios
├── docker-compose.yml            # Archivo de despliegue usando Docker Compose
└── README.md                     # Documentación general del proyecto
```

## Ejecución

Para ejecutar el microservicio user, sigue los pasos a continuación. Estos comandos te permitirán construir y ejecutar el contenedor Docker del microservicio en tu máquina local.

1. **Navega al directorio del microservicio:**

   Primero, asegúrate de estar dentro del directorio `user`:

   ```bash
   cd token-flask/user/
   ```

2. **Construye la imagen Docker:**
Ejecuta el siguiente comando para construir la imagen Docker del microservicio. Este comando utilizará el `Dockerfile` en el directorio `user` para crear la imagen: 
    ```bash
    docker build -t user_service .
    ```
    `-t user_service`: Etiqueta (tag) para la imagen Docker

3. **Ejecuta el contenedor Docker:**
Una vez que la imagen Docker se ha construido correctamente, puedes ejecutar el contenedor utilizando el siguiente comando:

    ```bash
    docker run -it -d -p 2000:2000 --name user_service_container user_service
    ```

    - `-it`: Permite la interacción con el contenedor si es necesario.

    - `-d`: Ejecuta el contenedor en segundo plano (modo "detached").

    - `-p 2000:2000`: Mapea el puerto 2000 del contenedor al puerto 2000 de tu máquina local.

    - `--name user_service_container`: Asigna un nombre al contenedor para facilitar su manejo.

    - `user_service`: Nombre de la imagen Docker creada previamente.

4. **Verifica que el contenedor esté en ejecución:**
    ```bash
    docker ps
    ```

    Esto mostrará una lista de los contenedores que se están ejecutando actualmente. Deberías ver `user_service_container` en la lista.


5. **Detener el contenedor:**

    Para detener el contenedor cuando hayas terminado de usarlo, ejecuta:

    ```bash
    docker stop user_service_container
    ```


## Uso

El microservicio `user` expone una API RESTful que permite la gestión de publicaciones en la aplicación. A continuación, se describen los principales endpoints y cómo utilizarlos:

### Endpoints Disponibles

## Uso

El servicio de gestión de usuarios permite crear, buscar, eliminar y consultar usuarios. A continuación, se describen los endpoints disponibles:

### 1. Creación de usuarios

Crea un usuario con los datos brindados. El nombre de usuario debe ser único, así como el correo.

- **Método:** `POST`
- **Ruta:** `/users`
- **Parámetros:** N/A
- **Encabezados:** N/A
- **Cuerpo:**
  ```json
  {
    "username": "nombre de usuario",
    "password": "contraseña del usuario",
    "email": "correo electrónico del usuario",
    "dni": "identificación",
    "fullName": "nombre completo del usuario",
    "phoneNumber": "número de teléfono"
  } 
  ```

- **Respuestas:**

| Código | Descripción                                                                      | Cuerpo                                                 |
|--------|----------------------------------------------------------------------------------|--------------------------------------------------------|
| 400    | Alguno de los campos obligatorios no está presente o tiene un formato incorrecto. | N/A                                                    |
| 412    | El usuario con el `username` o el correo ya existe.                              | N/A                                                    |
| 201    | El usuario se ha creado con éxito.                                               | `{ "id": "id del usuario", "createdAt": "fecha en formato ISO" }` |



### 2. Actualización de usuarios

Actualiza los datos de un usuario con los datos brindados. Solo los valores de `fullName`, `phoneNumber`, `dni` y `status` son modificables.

- **Método:** `PATCH`
- **Ruta:** `/users/{id}`
- **Parámetros:** `id`: identificador del usuario.
- **Encabezados:** N/A
- **Cuerpo:**
  ```json
  {
    "status": "nuevo estado del usuario",
    "dni": "identificación",
    "fullName": "nombre completo del usuario",
    "phoneNumber": "número de teléfono"
  }
  ```

- **Respuestas:**

| Código | Descripción                                              | Cuerpo                                     |
|--------|----------------------------------------------------------|--------------------------------------------|
| 400    | La petición no contiene al menos uno de los campos esperados. | N/A                                        |
| 404    | El usuario con el `id` especificado no existe.           | N/A                                        |
| 200    | El usuario se ha actualizado con éxito.                  | `{ "msg": "el usuario ha sido actualizado" }` |


### 3. Generación de token

Genera un nuevo token para el usuario correspondiente al `username` y `password`.

- **Método:** `POST`
- **Ruta:** `/users/auth`
- **Parámetros:** N/A
- **Encabezados:** N/A
- **Cuerpo:**
  ```json
  {
    "username": "nombre de usuario",
    "password": "contraseña del usuario"
  } 
  ```

- **Respuestas:**

| Código | Descripción                                             | Cuerpo                                                         |
|--------|---------------------------------------------------------|----------------------------------------------------------------|
| 400    | Alguno de los campos no está presente en la solicitud.  | N/A                                                            |
| 404    | El usuario con el `username` y `password` especificados no existe. | N/A                                                            |
| 200    | Token generado con éxito.                               | `{ "id": "id del usuario", "token": "Token generado", "expireAt": "fecha en formato ISO" }` |



### 4. Consultar información del usuario

Retorna los datos del usuario asociado al token.

- **Método:** `GET`
- **Ruta:** `/users/me`
- **Parámetros:** N/A
- **Encabezados:**
  - `Authorization: Bearer token`
- **Cuerpo:** N/A

- **Respuestas:**

| Código | Descripción                                 | Cuerpo                                                                                           |
|--------|---------------------------------------------|--------------------------------------------------------------------------------------------------|
| 401    | El token no es válido o está vencido.       | N/A                                                                                              |
| 403    | No hay token en la solicitud.               | N/A                                                                                              |
| 200    | Información del usuario retornada con éxito. | `{ "id": "id del usuario", "username": "nombre de usuario", "email": "correo electrónico", "fullName": "nombre completo", "dni": "número de identificación", "phoneNumber": "número de contacto", "status": "estado" }` |


### 5. Consulta de salud del servicio

Usado para verificar el estado del servicio.

- **Método:** `GET`
- **Ruta:** `/users/ping`
- **Parámetros:** N/A
- **Encabezados:** N/A
- **Cuerpo:** N/A

- **Respuestas:**

| Código | Descripción                                | Cuerpo  |
|--------|--------------------------------------------|---------|
| 200    | Confirmación de que el servicio está activo. | `pong`  |


### 6. Restablecer base de datos

Usado para limpiar la base de datos del servicio.

- **Método:** `POST`
- **Ruta:** `/users/reset`
- **Parámetros:** N/A
- **Encabezados:** N/A
- **Cuerpo:** N/A

- **Respuestas:**

| Código | Descripción                             | Cuerpo                                        |
|--------|-----------------------------------------|-----------------------------------------------|
| 200    | Todos los datos fueron eliminados.      | `{ "msg": "Todos los datos fueron eliminados" }` |

## Pruebas

Para ejecutar las pruebas unitarias del microservicio `user` y verificar que el código cumpla con los requisitos de calidad, sigue los pasos a continuación.

### Requisitos previos

Asegúrate de haber configurado correctamente las variables de entorno necesarias (`.env.test`) y de tener todas las dependencias instaladas usando `pipenv`.

### Comandos para ejecutar las pruebas

1. **Activar el entorno virtual:**

   Antes de ejecutar las pruebas, asegúrate de activar el entorno virtual con pipenv:

   ```bash
   pipenv shell
   ```
2. **Asegurate de estar en el directorio correcto:**
  Asegurate de encontrarte en el directorio `cd token-flask/user/`

3. **Ejecutar las pruebas unitarias:**

    Ejecuta las pruebas unitarias y asegúrate de que la cobertura de código sea del 70% o más:

      ```bash
      pytest --cov-fail-under=70 --cov=src
      ```

4. **Generar reporte de cobertura de pruebas:**
    Si deseas generar un reporte HTML con la cobertura de las pruebas, utiliza el siguiente comando:

    ```bash
    pytest --cov-fail-under=70 --cov=src --cov-report=html
      ```
    Este comando generará un directorio htmlcov en tu proyecto, que contendrá un archivo index.html que puedes abrir en tu navegador para ver el reporte detallado de la cobertura de código.


## Otras Características (opcional)

Este proyecto de microservicio tiene las siguientes características adicionales que pueden ser útiles:

- **Persistencia en PostgreSQL:** El microservicio utiliza una base de datos PostgreSQL para almacenar y gestionar los datos de las publicaciones.
- **Manejo de Errores:** Implementa un manejo de errores robusto para asegurar respuestas claras y útiles a los usuarios finales y a otros servicios.
- **Despliegue en Docker:** El microservicio está configurado para ejecutarse en contenedores Docker, facilitando su despliegue en diferentes entornos.

## Autor
Este microservicio fue desarrollado por:

- **Camilo Lesmes** - [GitHub](https://github.com/lesmesl)
