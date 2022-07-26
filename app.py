from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_session import Session


app = Flask(__name__)

TEMPLATES_AUTO_RELOAD = True
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'magazines'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL(app)


@app.route('/')
def index():
    if session.get('loggedin'):
        user = {
            'id': session.get('id'),
            'email': session.get('email'),
            'f_name': session.get('f_name'),
            'l_name': session.get('l_name')
        }
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT magazine_tbl.id, magazine_tbl.title, magazine_tbl.description, magazine_tbl.user_id, user_tbl.f_name, user_tbl.l_name FROM magazine_tbl LEFT JOIN user_tbl ON user_tbl.id=magazine_tbl.user_id ')
        magazines = cursor.fetchall()
        return render_template('index.html', user=user, magazines=magazines, link='home')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user_tbl WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            session['f_name'] = account['f_name']
            session['l_name'] = account['l_name']
            res = {'status': 200, 'msg': 'Logged in successfully !'}
            return res
        else:
            res.status = 200
            res.msg = 'Incorrect email / password !'
            return res
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user_tbl WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            res = {'status': 400, 'msg': 'Account already exists !'}
            return res
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            res = {'status': 400, 'msg': 'Invalid email address !'}
            return res
        elif not re.match(r'[A-Za-z0-9]+', email):
            res = {'status': 400,
                   'msg': 'Email must contain only characters and numbers !'}
            return res
        elif not email or not password or not email:
            res = {'status': 400, 'msg': 'Please fill out the form !'}
            return res
        else:
            cursor.execute(
                'INSERT INTO user_tbl VALUES (NULL, % s, % s, % s, % s)', (f_name, l_name, email, password))
            mysql.connection.commit()
            res = {'status': 200, 'msg': 'You have successfully registered !'}
            return res
    elif request.method == 'POST':
        res = {'status': 400, 'msg': 'Please fill out the form !'}
        return res
    return render_template('register.html')

@app.route('/new-magazine', methods=['GET', 'POST', 'DELETE'])
def newMagazine():
    if not session.get('loggedin'):
        return redirect(url_for('login'))

    if request.method == 'POST' and 'title' in request.form:
        title = request.form['title']
        description = request.form['description']
        id = session.get('id')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
                'INSERT INTO magazine_tbl VALUES (NULL, % s, % s, % s)', (id, title, description))
        mysql.connection.commit()
        res = {'status': 200, 'msg': 'New magazine is successfully added !', 'id': cursor.lastrowid}
        return res
    elif request.method == 'POST':
        res = {'status': 400, 'msg': 'Please fill out the form !'}
        return res
    return render_template('add-new.html', link='new-magazine')

@app.route('/magazine/<int:m_num>', methods=['GET', 'DELETE'])
def magazineDetail(m_num):
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        str_num = str(m_num)
        cursor.execute(
                'SELECT magazine_tbl.id, magazine_tbl.title, magazine_tbl.description, magazine_tbl.user_id, user_tbl.f_name, user_tbl.l_name FROM magazine_tbl LEFT JOIN user_tbl ON user_tbl.id=magazine_tbl.user_id WHERE magazine_tbl.id=%s', [str_num])
        magazine = cursor.fetchone()
        print(magazine)
        return render_template('detail.html', magazine=magazine)
    elif request.method == 'DELETE':
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            str_num = str(m_num)
            cursor.execute(
                    'DELETE FROM magazine_tbl WHERE id=%s', [str_num])
            mysql.connection.commit()
            res = {'status': 200, 'msg': 'Deleted successfully!'}
            return res
        except:
            res = {'status': 400, 'msg': 'Deleting failed!'}
            return res

@app.route('/account', methods=['GET', 'POST'])
def account():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session.get('id')
    if request.method == 'POST' and 'email' in request.form:
        try:
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            email = request.form['email']
            print(f_name, l_name, email, user_id)
            cursor.execute(
                    'UPDATE user_tbl SET email=%s, f_name=%s, l_name=%s WHERE id=% s', (email, f_name, l_name, str(user_id)))
            mysql.connection.commit()
            session['email'] = email
            session['f_name'] = f_name
            session['l_name'] = l_name
            res = {'status': 200, 'msg': 'Updated successfully!'}
            return res
        except:
            res = {'status': 400, 'msg': 'Updating failed!'}
            return res
    else:
        user = {
                'id': session.get('id'),
                'email': session.get('email'),
                'f_name': session.get('f_name'),
                'l_name': session.get('l_name')
            }
        print(user_id)
        cursor.execute(
                'SELECT * from magazine_tbl where user_id=% s', str(user_id))
        magazines = cursor.fetchall()
        return render_template('account.html', magazines=magazines, user=user, link='account')

if __name__ == "__main__":
    app.run(debug=True)
