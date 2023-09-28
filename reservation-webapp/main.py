import MySQLdb.cursors
from flask import Flask, request, render_template, url_for, redirect, session, flash
from flask_mysqldb import MySQL
import re
import os




app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsecret'
app.config['MYSQL_DB'] = 'clouddb2'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/restaurants")
def restaurants_list():
    return render_template('restaurant_list.html')

@app.route("/restaurant/abc") #replace abc dynamically, restaurant remains static
def restaurant_profile():
    return render_template('restaurant_profile.html')

@app.route("/form", methods=['GET', 'POST'])
def particulars_form():
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        size = request.form['size']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO particulars VALUES (NULL, %s, %s, %s, %s)", (name, phone, email, size))
        cursor.connection.commit()
        cursor.close()
    return render_template('particulars_form.html')

if __name__ == '__main__':
    app.run(debug=True)