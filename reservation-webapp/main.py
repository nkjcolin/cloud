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

@app.route('/', methods=['GET', 'POST'])
def search_restaurants():
    # Get form data
    search_query = request.form.get('search_query')
    dietary_needs = request.form.get('dietary_needs')
    meal_type = request.form.get('meal_type')

    # Create a cursor for executing SQL queries
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Build and execute the SQL query
    query = "SELECT * FROM restaurants WHERE name LIKE %s AND dietary_needs = %s AND meal_type = %s"
    cursor.execute(query, (f'%{search_query}%', dietary_needs, meal_type))

    # Fetch all matching rows
    results = cursor.fetchall()

    # Create a list to store restaurant data
    restaurant_data = []

    # Iterate through the results and extract relevant information
    for row in results:
        restaurant_info = {
            'name': row['name'],
            'dietary_needs': row['dietary_needs'],
            'meal_type': row['meal_type'],
            'timings': row['timings'],
            # Add more fields as needed
        }
        restaurant_data.append(restaurant_info)

    # Close the cursor and MySQL connection
    cursor.close()
    return render_template('restaurant_list.html', restaurant_data=restaurant_data)

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