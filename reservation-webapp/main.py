import MySQLdb.cursors
from flask import Flask, request, render_template, url_for, redirect, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsecret'
app.config['MYSQL_DB'] = 'clouddb2'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_HOST'] = 'aws-cloud-db.c51u88x7edpw.us-east-1.rds.amazonaws.com'
# app.config['MYSQL_PASSWORD'] = 'pmB6YW7fYDuRo0Be8sEJ'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

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
            'id': row['id'],
            'name': row['name'],
            'dietary_needs': row['dietary_needs'],
            'meal_type': row['meal_type'],
            'timings': row['timings'],
            'description': row['description'],
            # Add more fields as needed
        }
        restaurant_data.append(restaurant_info)

    # Close the cursor and MySQL connection
    cursor.close()
    return render_template('restaurants_view.html', restaurant_data=restaurant_data)

@app.route("/allrestaurants", methods=['GET'])
def restaurants_view():
    # Create a cursor for executing SQL queries
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Create a list to store restaurant data
    restaurant_data = []

    # Build and execute the SQL query
    query = "SELECT * FROM restaurants"
    cursor.execute(query)

    # Fetch all matching rows
    results = cursor.fetchall()

    # Show all result
    for row in results:
        restaurant_info = {
            'id': row['id'],
            'name': row['name'],
            'dietary_needs': row['dietary_needs'],
            'meal_type': row['meal_type'],
            'timings': row['timings'],
            'description': row['description'],
            # Add more fields as needed
        }
        restaurant_data.append(restaurant_info)
    # Close the cursor and MySQL connection
    cursor.close()
    return render_template('restaurants_view.html', restaurant_data=restaurant_data)

@app.route("/restaurant/<int:id>")
def restaurant_profile(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM restaurants WHERE id = %s', (id,))
    restaurant_data = cursor.fetchone()
    cursor.close()
    return render_template('restaurant_profile.html', restaurant_data=restaurant_data)


@app.route("/form", methods=['POST'])
def particulars_form():
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        timing = request.form['timing']
        size = request.form['size']

        # Save the form data in a dictionary
        form_data = {
            'name': name,
            'phone': phone,
            'email': email,
            'timing': timing,
            'size': size,
        }

        # Assuming you have a success.html template
        return render_template('success.html', form_data=form_data)

    # Handle GET requests or other cases
    return render_template('error.html')  # You can create an error.html template for error cases


if __name__ == '__main__':
    app.run(debug=True)
    # make it accessible from your host machine when dockerising the app 
    #app.run(host='0.0.0.0', port=5000)
