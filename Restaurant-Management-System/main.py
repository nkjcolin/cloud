import MySQLdb.cursors
from flask import Flask, request, render_template, url_for, redirect, session, flash
from datetime import datetime
from flask_mysqldb import MySQL
import re
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MY_APP_SECRET_KEY')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')

# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')

app.config['MYSQL_CURSORCLASS'] = os.getenv('MYSQL_CURSORCLASS')
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO newsletters VALUES (NULL, %s, %s, %s)", (firstname, lastname, email))
        cursor.connection.commit()
        cursor.close()
    return render_template('home.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/menu')
def menu_page():
    return render_template('menu.html')


@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html')


@app.route('/contact', methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO support VALUES (NULL, %s, %s, %s, %s, %s)",
                       (firstname, lastname, phone, email, message))
        cursor.connection.commit()
        cursor.close()
    return render_template('contact.html')


@app.route('/book_a_table', methods=["GET", "POST"])
def booking_page():
    current_day = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        name = request.form['name']
        nr_guests = request.form['nr_guests']
        email = request.form['email']
        phone = request.form['phone']
        time = request.form['time']
        date = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO bookings VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                       (date, time, name, email, phone, nr_guests))
        cursor.connection.commit()
        cursor.close()
    return render_template('reservations.html', current_day=current_day)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        category = request.form['category']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s AND category = %s",
                       (username, password, category))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['category'] = user['category']
            return render_template('admin_interface/admin_main.html')
        else:
            flash("Wrong username and/or password. Please try again!")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin_main')
def admin_main_page():
    if 'loggedin' in session:
        return render_template('admin_interface/admin_main.html')
    else:
        return redirect('login.html')


@app.route('/online_reservations')
def admin_reservations():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
        reservation_list = cursor.fetchall()
        return render_template('admin_interface/admin_reservations.html', reservation_list=reservation_list)


@app.route('/client_support')
def admin_support_page():
    if 'loggedin' in session and 'admin' in session['username']:
        return render_template('admin_interface/admin_support.html')
    elif 'loggedin' in session and 'admin' not in session['username']:
        return redirect(url_for('admin_main_page'))
    else:
        return redirect(url_for('login'))


@app.route('/employees')
def employees():
    if 'loggedin' in session and 'admin' in session['username']:
        return render_template("admin_interface/admin_employees.html")
    elif 'loggedin' in session and 'admin' not in session['username']:
        return redirect(url_for('admin_main_page'))
    else:
        return redirect(url_for('login'))


@app.route('/subscribers')
def subscribers():
    if 'loggedin' in session and 'admin' in session['username']:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM newsletters ORDER BY id DESC")
        subscribers_list = cursor.fetchall()
        return render_template("admin_interface/admin_subscribers.html", subscribers_list=subscribers_list)
    elif 'loggedin' in session and 'admin' not in session['username']:
        return redirect(url_for('admin_main_page'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
