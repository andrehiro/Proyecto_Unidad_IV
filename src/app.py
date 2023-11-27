from functools import wraps
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import config
from flask_mysqldb import MySQL
from models import ModelProductos
from models.ModelUsers import ModelUsers
from models.entities.users import User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

@app.route("/")
def index():
    return redirect("login")


@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'],0)
        logged_user = ModelUsers.login(db, user)
        if logged_user != None:
            login_user(logged_user)
            if logged_user.usertype == 1:
                session['admin'] = True
                return redirect(url_for("admin"))
            else:
                session['admin'] = False
                return redirect(url_for("inicio"))
        else:
            flash("Acceso rechazado...")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
# Verificar si el usuario está autenticado y es un administrador
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403) # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view

@app.route("/admin")
@login_required
@admin_required
def admin():
   is_admin = current_user.usertype == 1 if current_user.is_authenticated else False
   return render_template("inicio.html", is_admin=is_admin)

@app.route("/acercaDe")
@login_required
def acercaDe():
    return render_template("acercaDe.html")

@app.route("/catalogo")
@login_required
@admin_required
def catalogo():
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, nombre, imagen, precio FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return render_template("catalogo.html", productos=productos)

@app.route("/usuarios")
@login_required
@admin_required
def usuarios():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM users")
    usuarios = cursor.fetchall()
    cursor.close()
    print(usuarios)  # Imprimir los usuarios en la consola para verificar
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/tienda")
@login_required
def tienda():
    return render_template("tienda.html")

@app.route("/ticket")
@login_required
def ticket():
    return render_template("ticket.html")

@app.route("/inicio")
@login_required
def inicio():
    return render_template("inicio.html")

@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        fullname = request.form["fullname"]
        usertype = request.form["usertype"]

        cursor = db.connection.cursor()
        cursor.callproc("sp_AddUser", (username, password, fullname, usertype))
        db.connection.commit()
        cursor.close()

        return redirect("/usuarios")
    
@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    if request.method == "POST":
        user_id = request.form["user_id"]

        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.connection.commit()
        cursor.close()

        return redirect("/usuarios")

@app.route("/modificar_usuario", methods=["POST"])
def modificar_usuario():
    if request.method == "POST":
        user_id = request.form["user_id"]
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        new_fullname = request.form["new_fullname"]
        new_usertype = request.form["new_usertype"]

        cursor = db.connection.cursor()

        if new_password:
            cursor.execute("UPDATE users SET username = %s, password = %s, fullname = %s, usertype = %s WHERE id = %s",
                           (new_username, new_password, new_fullname, new_usertype, user_id))
        else:
            cursor.execute("UPDATE users SET username = %s, fullname = %s, usertype = %s WHERE id = %s",
                           (new_username, new_fullname, new_usertype, user_id))

        db.connection.commit()
        cursor.close()

        return redirect("/usuarios")
    
    
@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        imagen = request.form["imagen"]
        precio = request.form["precio"]

        cursor = db.connection.cursor()
        cursor.callproc("sp_AddProduct", (nombre, imagen, precio))
        db.connection.commit()
        cursor.close()

        return redirect("/catalogo")
    
@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    producto_id = request.form["producto_id"]
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    db.connection.commit()
    cursor.close()

    return redirect("/catalogo")

@app.route("/modificar_producto", methods=["POST"])
def modificar_producto():
    if request.method == "POST":
        producto_id = request.form["producto_id"]
        new_nombre = request.form["new_nombre"]
        new_imagen = request.form["new_imagen"]
        new_precio = request.form["new_precio"]

        cursor = db.connection.cursor()
        cursor.execute("UPDATE productos SET nombre = %s, imagen = %s, precio = %s WHERE id = %s",
                       (new_nombre, new_imagen, new_precio, producto_id))
        db.connection.commit()
        cursor.close()

        return redirect("/catalogo")
    
@app.route('/obtener_productos')
def obtener_productos():
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, nombre, imagen, precio FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    return jsonify(productos)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()