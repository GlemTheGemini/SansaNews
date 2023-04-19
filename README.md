# SansaNews

Aquí una pequeña guía de como inicializar el proyecto, y de los principales archivos que hay.

## Tabla de Contenidos

- [Pre-requisitos](#pre-requisitos)
- [Como Iniciar el Proyecto](#como-iniciar-el-proyecto)
  - [Configurando Python](#configurando-python)
  - [Paquetes](#paquetes)
  - [Iniciar Server](#iniciar-server)
- [Archivos Importantes](#archivos-importantes)
  - [Archivos Frontend](#archivos-frontend)
  - [Archivos Backend](#archivos-backend)
- [Importante](#importante)

## Pre-requisitos

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Como Iniciar el Proyecto

Primero debes de clonar el repositorio en tu PC con este comando:

``` shell
git clone https://github.com/GlemTheGemini/SansaNews.git
# Clona el repositorio en la carpeta actual
```

Por ultimo entra a la carpeta del repositorio con la terminal.

### Configurando Python

Antes de hacer cualquier cosa hay que instalar los paquetes de python que se ocupan en el proyecto, y para eso es recomendable primero usar un entorno virtual ([virtual environment](https://docs.python.org/3/library/venv.html)), para usamos:

``` shell
python -m venv  ./.venv # Windows
python3 -m venv ./.venv # Linux
# Crea un entorno virtual donde instalar los paquetes
```

Para activar el entorno virtual hay que poner en la terminal al inicio de cada sesión este comando:

``` shell
.\.venv\bin\Activate.ps1 # Windows
source .venv/bin/activate
# Activa el entorno virtual
```

Eso si tienes que estar seguro que tu editor de código está ocupando el espacio virtual, debería de aparecer algo así en vscode estando en un archivo de python.

![venv](docs/Screenshot%202023-04-18%20194222.png)

Sino tienes que elegir el interprete con la ubicación en la carpeta .venv recién creada.

![venv2](docs/Screenshot%202023-04-18%20201449.png)

### Paquetes

Por ultimo instalaremos los paquetes que usamos en el proyecto, estos son [django](https://docs.djangoproject.com/en/4.2/), [instaloader](https://instaloader.github.io/) y [crispy forms](https://pypi.org/project/django-crispy-forms/), se instalan mediante:

``` shell
pip install django instaloader django-crispy-forms
```

Aparte usamos [Bootstrap 5](https://getbootstrap.com/docs/5.1/getting-started/introduction/) para ponerle estilos a SansaNews.

### Iniciar Server

Por ultimo para iniciar el server y probar los cambios se ocupa el comando:

``` shell
python manage.py runserver
# Inicia el proyecto en un servidor local
```

La url con la ip que te tire, al abrirla en el navegador, podrás ver el proyecto y los cambios en tiempo real.

## Archivos Importantes

Aquí una lista con que hace cada uno de los archivos más importantes para el proyecto.

### Archivos Frontend

- `SansaNews/templates/` contiene los html del proyecto
- `SansaNews/templates/base.html` el html base de todas las paginas de SansaNews, contiene el header y el footer.
- `SansaNews/templates/Home.html` pagina inicial de SansaNews, extiende a `base.html`.
- `SansaNews/templates/Molde.html` html molde de las paginas de las iniciativas, extiende a `base.html`.
- `static/index.css` archivo principal de estilos de SansaNews.
- `static/navstyle.css` archivo de estilo para el header.

### Archivos Backend

- `SansaNews/templates/Test.html` html de prueba que actualiza las publicaciones de las iniciativas, se accede poniendo la url `/Test`.
- `SansaNews/API.py` archivo que se encarga de toda la logica de mantener actualizadas las publicaciones de las iniciativas.
- `SansaNews/iniciativas.py` archivo que contiene un diccionario con los usuarios de las iniciativas que estarán en la pagina.
- `static/iniciativas/` contiene las las publicaciones y la información de las iniciativas que se encuentran en SansaNews.

## Importante

- No ocupen mucho el `Test.html` que la API de Instagram tiene usos diarios limitados, más [aquí](https://instaloader.github.io/troubleshooting.html).
- Cuando esten avanzando en una nueva cosa, no suban los cambios altiro a la rama `main`, creen una aparte para ir probando los cambios, y cuando esten listos la fusionan con el `main`.
