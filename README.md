# Plantilla para Microservicio de Generación de Token de Usuario

Este proyecto es una plantilla para un microservicio de usuarios que permite la generación y gestión de tokens de autenticación.

| Nombre             | Correo                         |
|--------------------|--------------------------------|
| Camilo Lesmes      | c.lesmesl@uniandes.edu.co      |

## Microservicio Implementado

Se han desarrollado cuatro microservicios principales, cada uno exponiendo una API REST que permite gestionar las entidades clave del sistema:

1. **Gestión de Usuarios (`/users`)**: 
   - Registro y verificación de usuarios.
   - Actualización de perfiles.
   - Autenticación mediante tokens.
   - Actualización del estado de un usuario.

## Pre-requisitos

Para ejecutar correctamente los microservicios, asegúrate de contar con los siguientes componentes:

- **Python** ~3.9
- **pipenv**  
  - Ejecuta `pip install pipenv` para instalarlo.
- **Docker**
- **Docker Compose**
- **Postman** (para pruebas de las APIs)
- **PostgreSQL**
  - Las instrucciones de instalación pueden variar según el sistema operativo. Consulta la [documentación oficial de PostgreSQL](https://www.postgresql.org/download/). Si estás en un sistema Unix, te recomendamos utilizar [Homebrew](https://wiki.postgresql.org/wiki/Homebrew).

## Ejecución del Microservicio local

Antes de empezar se deve tener instalado `pipenv` con Python 3.9. Luego realizar estos pasos

    ```bash
    # 1. Clonar el repositorio
    # 2. Ingresar a la carpeta de usuario
    $ cd user
    # 3. Instalar las dependencias
    $ pipenv install
    # 4. Activar el entorno virtual
    $ pipenv shell
    # Nota: Si usas vscode seleccionar en el interprete de python la ruta del entorno virtual
    ```

### Estructura de la carpeta `src`

La carpeta `src` contiene el código fuente del microservicio. Sus subdirectorios principales son:

- **`/models`**: Contiene la capa de persistencia y los modelos que serán almacenados en la base de datos. El archivo `model.py` incluye un modelo base (`Model`) que define columnas comunes como `createdAt` y `updatedAt`.
  
- **`/commands`**: Almacena la lógica de negocio implementada usando un patrón de diseño de comandos. Cada comando hereda de la clase `BaseCommand` (ubicada en `commands/base_command.py`) y debe implementar el método `execute`.

- **`/blueprints`**: Contiene la capa de aplicación que declara y expone los servicios API del microservicio.

- **`/errors`**: Define excepciones personalizadas para manejar errores HTTP y devolver los códigos de estado adecuados.

### Variables de Entorno

El servidor Flask y las pruebas utilizan variables de entorno para configurar las credenciales de la base de datos y otros ajustes. A continuación, las variables principales:

- `DB_USER`: Usuario de la base de datos PostgreSQL.
- `DB_PASSWORD`: Contraseña de la base de datos PostgreSQL.
- `DB_HOST`: Host de la base de datos PostgreSQL.
- `DB_PORT`: Puerto de la base de datos PostgreSQL.
- `DB_NAME`: Nombre de la base de datos PostgreSQL.
- `USERS_PATH`: Ruta del microservicio de Usuarios para interactuar con los endpoints de usuarios.

Estas variables deben especificarse en los archivos `.env.development` y `.env.test`.

### Ejecución de Pruebas

Para ejecutar pruebas unitarias y verificar la cobertura de código, puedes usar los siguientes comandos:

```bash
pytest --cov-fail-under=70 --cov=src
pytest --cov-fail-under=70 --cov=src --cov-report=html
```

## Ejecución con Docker y Docker Compose

### Ejecutar con Docker Compose

Para ejecutar todos los microservicios de manera simultánea, puedes utilizar `docker-compose`. Para construir y levantar los servicios, utiliza el siguiente comando:

```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

### Ejecutar el Contenedor Docker

Una vez que la imagen Docker ha sido construida correctamente, puedes ejecutar el contenedor con el siguiente comando:

```bash
docker run -it -d -p <PUERTO_LOCAL>:<PUERTO_CONTENEDOR> --name <NOMBRE_DEL_CONTENEDOR> <NOMBRE_DE_LA_IMAGEN>
```

#### Ejemplo para el Microservicio de Usuarios

```bash
# Microservicio de Usuarios
$> docker run -it -d -p 3000:3000 --name user_service_container user_service
```

Este markdown está más organizado y claro, con secciones bien definidas y fácil de seguir.