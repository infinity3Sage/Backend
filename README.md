# Backend
Proyecto Django para I3 web

# Requisitos para el proyecto Django

- Tener instalado Python 3 y PIP
    * Python 3 se debe descargar e instalar de su página oficial: https://www.python.org/downloads/
    * Comprueba primero que no tengas PIP instalado en tu terminal "pip --version". Si no lo tienes, PIP deberá instalarse ejecutando los siguientes comandos
       > curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
       > python get-pip.py
       > pip --version
       
- Tener instalado virtualenv usando "pip install virtualenv"
- Tener instalado servidor postgrSQL y crear por terminal una base de datos con la siguiente información: --> **En el excel de conexiones hay una posible configuración por si se quiere usar**
  * User	(el que tu quieras para tu base de datos en local) 
  * Pass	(La que tu consideres para tu base de datos en local)
  * Host	localhost
  * Puerto	5432
  * Base de datos	infinity3

# Configuración proyecto

- Cuando se realice el pull por primera vez, se deberá crear un entorno virtual usando python. Para ello deberá situarse en la carpeta raíz del proyecto y ejecutar el siguiente comando "virtualenv env"
- Una vez creada la carpeta env, deberemos entrar al entorno virtual para instalar los requerimientos:
  * En Linux o Mac, active el nuevo entorno python: source env/bin/activate
  * O en Windows: .\env\Scripts\activate
  * Instala los requirements: pip instal -r requirements.txt
    
- Una vez configurado todo, se deberá crear el fichero ".env" en el directorio raíz con las variables de entorno para que settings.py pueda usarlas. Dentro de el definiremos como minimo las variables por defecto:
  * SECRET_KEY='secret key' (Abre una terminal o un entorno interactivo de Python. Ejecuta el siguiente código para generar una clave secreta: import secrets; print(secrets.token_urlsafe(50));)
  * DEBUG=True
  * DB_NAME=infinity3
  * DB_USER=postgres (o el usaurio que tu hayas creado)
  * DB_PASSWORD=G#8fW2q@9bL!jZ4pV5m^1x$R (O la pass que tu hayas definido)
  * DB_HOST=localhost
  * DB_PORT=5432
  * ALLOWED_HOST_DEV=*
  * ALLOWED_HOST_DEPLOY=django.infinity3.es www.infinity3.es
  * CORS_ORIGIN_WHITELIST_DEV=http://localhost:3000 http://localhost:3001
  * CORS_ORIGIN_WHITELIST_DEPLOY=https://www.infinity3.es https://infinity3.es https://django.infinity3.es
  * CSRF_TRUSTED_ORIGINS_DEV=http://localhost:3000 http://localhost:3001
  * CSRF_TRUSTED_ORIGINS_DEPLOY=https://www.infinity3.es https://infinity3.es https://django.infinity3.es
  * SUSCRIPCION_NIVELES=FREE:Free BASIC:Basic PRO:Pro INFINITY:Infinity
  * LIMITE_USUARIOS_FREE=1
  * LIMITE_USUARIOS_BASIC=10
  * LIMITE_USUARIOS_PRO=60
  * LIMITE_USUARIOS_INFINITY=200
    
- Ajustar configuración del core (settings.py) por si faltase alguna cosa para desplegar en local

# Subida a producción

- Para subir a la rama deploy se deberán de subir todos los ficheros exceptuando el .gitignore y el setting.py ya que cada rama debería de tener el suyo. **Únicamente se subirán los cambios de settings.py cuando se haya tocado alguna cosa que se deba migrar a producción, y NUNCA se subirá el fichero completo, si nosolo los cambios realizados ya que las variables deben seguiir apuntando al servidor de producción**
- **¡¡OJO!!** si hemos instalado alguna librería más que no esté en producción pon pip install, se deberá de instalar también en el entorno virtual del servidor de producción cuando se desplieguen cambios.
