
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key='qwerty'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='tp2_db'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    mesage=''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user: 
            session['loggedin']=True
            session['userid']=user['userid']
            session['username']=user['name']
            session['email']=user['email']
            mesage = 'Bienvenido'
            return render_template('user.html', mesage=mesage)
        else:
            mesage='Por favor ingrese un email o contraseña correcta'
    return render_template('login.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage=''
    if request.method == 'POST' and 'redname' in request.form and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        nombrered=request.form['redname']
        userName=request.form['name']
        password=request.form['password']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account=cursor.fetchone()
        if account:
            mesage='Cuenta ya Existe'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage='Email invalido'
        elif not nombrered or not userName or not password or not email:
            mesage='Por favor inserte el dato que falta'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s)', (nombrered, userName, email, password, ))
            mysql.connection.commit()
            mesage='Cuenta creada satisfactoriamente'
        return render_template('user.html', mesage=mesage)

    elif request.method == 'POST':
        mesage='Por favor complete el formulario'
    return render_template('register.html', mesage=mesage)

if __name__=="__main__":
    app.run()


