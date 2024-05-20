# SansaNews

Aquí una pequeña guía de como inicializar el proyecto, y de los principales archivos que hay.


## Tabla de Contenidos

- [Pre-requisitos](#pre-requisitos)
- [Como Iniciar el Proyecto](#como-iniciar-el-proyecto)
  - [Configurando Python](#configurando-python)
  - [Paquetes](#paquetes)
  - [Iniciar Server](#iniciar-server)
  - [Login a la cuenta de Instagram](#login-a-la-cuenta-de-instagram)
- [Archivos Importantes](#archivos-importantes)
  - [Archivos Frontend](#archivos-frontend)
  - [Archivos Backend](#archivos-backend)
- [Links de Debug](#links-de-debug)
  - [En el home](#en-el-home)
  - [En las páginas de iniciativas](#en-las-paginas-de-iniciativas)


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
.\.venv\Scripts\Activate.ps1 # Windows
source .venv/bin/activate # Linux
# Activa el entorno virtual
```

Eso si tienes que estar seguro que tu editor de código está ocupando el espacio virtual, debería de aparecer algo así en vscode estando en un archivo de python.

![venv](docs/Screenshot%202023-04-18%20194222.png)

Sino tienes que elegir el interprete con la ubicación en la carpeta .venv recién creada.

![venv2](docs/Screenshot%202023-04-18%20201449.png)

### Paquetes

Por ultimo instalaremos los paquetes que usamos en el proyecto, estos son;:

- [django](https://docs.djangoproject.com/en/4.2/), 
- [instagrapi](https://subzeroid.github.io/instagrapi/)
- [crispy forms](https://pypi.org/project/django-crispy-forms/)

se instalan mediante:

``` shell
pip install django instagrapi pillows django-crispy-forms
```

Aparte usamos [Bootstrap 5](https://getbootstrap.com/docs/5.1/getting-started/introduction/) para ponerle estilos a SansaNews.

### Iniciar Server

Por ultimo para iniciar el server y probar los cambios se ocupa el comando:

``` shell
python manage.py runserver
# Inicia el proyecto en un servidor local
```

La url con la ip que te tire, al abrirla en el navegador, podrás ver el proyecto y los cambios en tiempo real.

### Login a la cuenta de Instagram

Uno tiene más intentos y más margen si se logea a una cuenta de instagram en la api, por esto existe un script para logearse en la api de SansaNews en `SansaNews/api/login.py`, para ejecutarlo en la linea de comandos debes de poner:

``` shell
python SansaNews/api/login.py
```

Luego te pedira las credenciales para logearte en una cuenta de instagram, ponelas y este creara un archivo en `SansaNews/api/session.json` donde guardara la sesión de instagram para que no tengas que volver a logearte, es muy importante que este `session.json` no sea súbido al github ya que con este cualquiera puede entrar a la cuenta de instagram logeada.

Una vez logeado podras ocupar la api con más margen, pero de todas manera no la sobreocupes, que si Instagram llega a pensar que la cuenta es un bot nos pueden llegar a banear la cuenta.


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

- `SansaNews/api/iniciativa.py` parte de la api encargada de controlar la creacion, limpiado y actualizacion de las iniciativas del proyecto.
- `SansaNews/api/posts.py` parte de la api encargada de descargar posts, ordenarlos por más recientes, filtrarlos para el uso en el proyecto.
- `static/iniciativas/iniciativas.json` json que guarda la información de las iniciativas que se deben poner manualmente, si quieren poner más iniciativas se edita eso.
- `static/iniciativas/posts.json` json que guarda todos los posts descargados ordenados por más recientes.
- `static/iniciativas/` contiene las las publicaciones y la información de las iniciativas que se encuentran en SansaNews.


## Links de Debug

Existen algunos links usados para debuguear con la api de una forma más facil, por favor usarlos con precaución y moderación, que multiples llamadas a la api de Instagram pueden resultar en un baneo de la cuenta logeada.

En general usar poca cantidad de iniciativas para debuguear y no llamar más de 10 veces a la api de instagram por hora.

### En el home

- `/iniciativas/inicializar` inicializa las iniciativas encontradas en `static/iniciativas.json` que no tengan una carpeta en `static/iniciativas`, llama a la api de Instagram una vez por cada iniciativa no inicializada, usar con precaución.
- `/iniciativas/actualizar` actualiza los posts de todas las iniciativas en `static/iniciativa/iniciativas.json`, llama a la api una vez por cada iniciativa en `static/iniciativas/iniciativa.json`
- `/iniciativas/limpiar` borra las carpetas de iniciativas que ya no se encuentren en `static/iniciativa/iniciativas.json`, no llama a la api.

### En las páginas de iniciativas

- `{usuario}/perfil/actualizar` actualiza el perfil de la iniciativa, redescargando su biografia y su foto de perfil aunque no hayan sido cambiados, llama una vez a la api.
- `{usuario}/perfil/borrar` borra la información de la iniciativa y su foto de perfil, dejando los posts sin borrar, no llama a la api.
- `{usuario}/posts/actualizar` actualiza los posts de la iniciativa, descargando los nuevos, y borrando los viejos en caso de que se supere el límite de posts, llama una vez a la api.
- `{usuario}/posts/redescargar` fuerza la redescarga de los posts de la iniciativa, primero borra todos los posts, y luego descarga los más recientes, aunque hayan repetidos, llama a la api una vez.
- `{usuario}/posts/borrar/{post_id}` borra el post de la iniciativa indicado con el `{post_id}` el cual es la fecha en que se subio el post compactada, se puede encontrar inspeccionando el post en cuestión, si `{post_id}` es `todos` borra todos los posts de la iniciativa
