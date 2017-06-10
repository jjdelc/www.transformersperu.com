# www.transformersperu.com

Este repositorio contiene material para construír la web de 
http://www.transformersperu.com

# Cómo usar

Para iniciar es necesario tener Python3 instalado en la máquina.
Crear el virtualenv con Python3 y instalar las dependencias


```
$ python3 -m venv ./venv
$ ./venv/bin/activate
$ pip install -U pip
$ pip install wheels
$ pip install -r requirements.txt
```

## Configuración inicial:

Se necesita un archivo de configuración (provisto en `settings.example.yaml`)
que se debe ajustar con los siguientes valores:

```
AWS_ACCESS_KEY_ID: <AWS Access Key>
AWS_ACCESS_KEY_SECRET: <AWS Secret>
BUCKET_NAME: <Bucket name>
BUCKET_LOCATION: <Boto Location.instance>
CTX:
  analytics: <Google analytics UA-XXXX-1 code>
  title: <HTML Title tag>
```

* `AWS_ACCESS_KEY_ID`: Access Key del la cuenta con accesso al bucket S3
* `AWS_ACCESS_KEY_SECRET`: Secreto de la cuenta con accesso al bucket S3
* `BUCKET_NAME`: Nombre del bucket
* `BUCKET_LOCATION`: Región. El nombre de las opciones disponibles en `boto.s3.connection.Location` donde esté alojado dicho bucket
* `CTX.analytics`: El código de Google Analytics
* `CTX.title`: Título de la página, se usa en la equiqueta TITLE del HTML 


## Para compilar:

Con el virtualenv cargado, ejecutar el siguiente comando usando el archivo
settings.yaml con los valores configurados:

```
(venv)$ settings=settings.yaml python build.py
```

Va a crear una carpeta `built` con un archivo `index.html` y los contenidos
de `source/content`.

## Para subir al servidor:

Igual que para compular pero usando el script `deploy.py`

```
(venv)$ settings=settings.yaml python deploy.py
```

Va a subir todos los archivos dentro de `./built/` al bucket S3.