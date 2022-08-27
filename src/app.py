from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'qwerty'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'antiphish_db'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

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
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'rol' in request.form:
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM administrador_global WHERE correoAG = % s AND passwordAG = % s AND rol = % s', (email, password, rol, ))
        administrador_global = cursor.fetchone()
        if administrador_global:
            session['loggedin'] = True
            session['name'] = administrador_global['idAG']
            session['username'] = administrador_global['nombreAG']
            session['email'] = administrador_global['correoAG']
            session['rol'] = administrador_global['rol']
            mesage = 'Bienvenido'
            return redirect(url_for('user'))
        else:
            mesage = 'Por favor ingrese un email o contraseña correcta'
    return render_template('login.html', mesage=mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'email' in session and session['rol'] == "Administrador Global":
        return render_template('user.html')
    elif 'email' in session and session['rol'] == "Administrador de Red":
        return "Hola, esta es la pantalla para el admin de red"
    else:
        return "Hola, esta es la pantalla para el usuario"

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
            mesage = 'Cuenta ya Existe'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Email invalido'
        elif not userName or not password or not email or not rol:
            mesage = 'Por favor inserte el dato que falta'
        else:
            cursor.execute('INSERT INTO administrador_global VALUES (NULL,% s, % s, % s, % s)',
                           (userName, email, password, rol, ))
            mysql.connection.commit()
            mesage = 'Cuenta creada satisfactoriamente'
        return render_template('login.html', mesage=mesage)

    elif request.method == 'POST':
        mesage = 'Por favor complete el formulario'
    return render_template('register.html', mesage=mesage)


if __name__ == "__main__":
    app.run(debug=True)
