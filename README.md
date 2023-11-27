# Proyecto_Unidad_IV
Andre Alexander Hidrogo Rocha 27/11/2023 Tercera parte del login por medio de Flask

Pasos a seguir
Sesiones y Flask
Las sesiones son fundamentales para mantener la información del usuario entre distintas interacciones en un sitio web. En este caso, se usará Flask para gestionar estas sesiones.

Instalación de flask_login
Para iniciar, se debe instalar el paquete flask_login en el entorno virtual utilizando el siguiente comando:

bash
Copy code
pip install FLASK_LOGIN
Implementación en el código
Manejo de sesiones con Flask
En el archivo app.py, se realiza la importación de las clases y funciones necesarias desde el paquete flask_login. Estas incluyen LoginManager, login_user, logout_user, y login_required.

python
Copy code
from flask_login import LoginManager, login_user, logout_user, login_required
LoginManager: Esta clase es esencial para configurar la autenticación y administrar las sesiones de usuario en Flask.
login_user: Función para iniciar sesión de un usuario en el sistema luego de proporcionar credenciales válidas.
logout_user: Utilizada para cerrar la sesión de un usuario en la aplicación.
login_required: Decorador para rutas o vistas que requieren que el usuario esté autenticado para acceder.
Configuración de LoginManager
Se crea una instancia de LoginManager asociada a la aplicación Flask:

python
Copy code
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)
Actualización de la ruta /login
Una vez que se verifica que las credenciales del usuario son válidas, se establece la sesión utilizando login_user():

python
Copy code
if logged_user is not None:
    login_user(logged_user)
Cargador de usuario (user_loader)
Se define un user_loader para cargar los datos del usuario que ha iniciado sesión:

python
Copy code
@login_manager.user_loader
def load_user(user_id):
    return ModelUsers.get_by_id(db, user_id)
Atributo is_active
Se agrega un atributo is_active a la clase User para controlar la sesión. Para lograrlo, se hace que la clase User herede de UserMixin del paquete flask_login:

python
Copy code
from flask_login import UserMixin

class User(UserMixin):
    # ...
Uso en las plantillas HTML
Para mostrar los datos del usuario en home.html y admin.html: <h1>{{ current_user.fullname }}</h1>
Para el logout, se crea la ruta /logout y se utiliza el método logout_user(). También se agrega un enlace en las plantillas admin.html y home.html para realizar el logout.
Restricciones de acceso
Se implementa el decorador admin_required para permitir el acceso solo a usuarios autenticados y con privilegios de administrador.
