# Proyecto_Unidad_IV
Andre Alexander Hidrogo Rocha 27/11/2023 Tienda en linea con una base de datos en MySQL

## Requisitos de la aplicación

* Sistema operativo compatible (Windows, macOS, Linux)
* Versión de Python requerida (Preferentemente 3.7 o 3.8)
* Dependencias externas (Flask, MySQL Connector/Python)
* Microsoft developer tools (Visual Studio)
* Un navegador compatible (Chrome, Firefox, Safari, etc.)
* Acceso a una base de datos MySQL y sus credenciales correspondientes

## Instrucciones de instalación

### Configuración del entorno virtual

Crea un entorno virtual
``` bash
py -m venv env
```

Activar el entorno virtual
``` bash
env\Scripts\activate
```

Instala Flask, Flask-Login, Flask-MySQLdb y Flask-WTF en el entorno virtual
``` bash
pip install Flask
pip install Flask-Login
pip install Flask-MySQLdb
pip install Flask-WTF
```

### Configuración de la base de datos

Crea una base de datos MySQL para la tienda en línea utilizando el script de la carpeta "database".
Configura las credenciales de la base de datos en el código o en un archivo de configuración separado.

### Descargar el código fuente

Clona o descarga el repositorio de la aplicación y coloca la carpeta "src" en la carpeta donde creaste tu entorno virtual.

### Ejecución de la aplicación

Asignar el archivo principal
``` bash
set FLASK_APP=app.py
```

Ejecutar el servidor Flask
``` bash
python .\src\app.py
```

Acceder a la aplicación desde un navegador web a través de la URL proporcionada por Flask.

## Instrucciones de uso

Para acceder a la pagina primero deberas crear una cuenta en MySQL con el procedimiento sp_AddUser.
``` sql
call sp_AddUser("admin","123","juan perez",1);
```

Una vez tienes una cuenta deberas ingresar los datos de la misma en el login
![Texto alternativo](https://github.com/andrehiro/Proyecto_Unidad_IV/blob/main/Imagenes%20para%20el%20README/login.png?raw=true)
