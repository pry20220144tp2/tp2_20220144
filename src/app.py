from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import clasificador_randomforest
from flask_mysqldb import MySQL
from flask import Flask
from flask import Blueprint, flash, g
from flask import jsonify
from werkzeug.utils import secure_filename
from functools import wraps
from flask_login import LoginManager, login_user, logout_user, login_required
app = Flask(__name__)
app.secret_key = 'qwerty'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'antiphish_db'

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User
mysql = MySQL(app)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)



@app.route('/')
def indice():
    return render_template('indice.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/service')
def service():
    return render_template('service.html')


@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['nombre'], request.form['password'], request.form['rol'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('phishing'))
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template('login.html')
    else:
        return render_template('login.html')





@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/usuarios')
def usuarios():
    return render_template("usuarios.html")
    
@app.route('/empresas')
def empresas():
    return render_template("empresas.html")

@app.route('/roles')
def roles():
    return render_template("roles.html")

@app.route('/correo')
@login_required
def correo():
    return render_template("correo.html")

@app.route('/user')
@login_required
def user():
    if session['rol'] == "Administrador Global":
        return redirect(url_for('phishing'))
    elif session['rol'] == "Administrador de Red":
        return "Hola, esta es la pantalla para el admin de red"
    else:
        return "hola"



@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'rol' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        rol = request.form['rol']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM administrador_global WHERE correoAG = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'La cuenta ya existe'
        elif not userName:
            mesage = 'Por favor ingrese Nombre'
        elif not re.match(r'[a-zA-ZÀ-ÿ\\u00f1\\u00d1]+(\\s[a-zA-ZÀ-ÿ\\u00f1\\u00d1])*[a-zA-ZÀ-ÿ\\u00f1\\u00d1]+$', userName):
            mesage = 'El nombre solo puede tener letras y máximo 1 palabra'
        elif not email:
            mesage = 'Por favor ingrese Correo'
        elif not re.match(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$', email):
            mesage = 'Correo inválido'
        elif not password:
            mesage = 'Por favor ingrese Contraseña'
        elif rol == "Escoge una opción":
            mesage = 'Por favor escoja un rol'
        else:
            cursor.execute('INSERT INTO administrador_global VALUES (NULL,% s, % s, % s, % s)',
                           (userName, email, password, rol, ))
            mysql.connection.commit()
            mesage = 'Cuenta creada satisfactoriamente'
        return render_template('login.html', mesage=mesage)

    elif request.method == 'POST':
        mesage = 'Por favor complete el formulario'
    return render_template('register.html', mesage=mesage)


UPLOAD_FOLDER = '/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/result')
def result():

    urlname = request.args['name']
    res = clasificador_randomforest.getResult(urlname)
    return jsonify(res)


@app.route('/detalleurl')
def detalleurl():
    return render_template('detalleurl.html')


@app.route('/phishing', methods=['GET', 'POST'])
@login_required
def phishing():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
            return "false"
        file = request.files['file']
        if file.filename == '':
            flash('no select file')
            return 'false'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            contents = file.read()
            with open("files/URL.txt", "wb") as f:
                f.write(contents)
            file.save = (os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return render_template("index.html")

    return render_template("index.html")

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == "__main__":
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug=True)
