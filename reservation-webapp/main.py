import MySQLdb.cursors
from flask import Flask, request, render_template, url_for, redirect, session, flash
from flask_mysqldb import MySQL
import grpc
import booking_pb2
import booking_pb2_grpc

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretsecret'
app.config['MYSQL_DB'] = 'clouddb2'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_HOST'] = 'clouddb2.ccmmflq8mlun.us-east-2.rds.amazonaws.com'
app.config['MYSQL_PASSWORD'] = 'w8wIarTDECzxLq$'

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_HOST'] = 'localhost'

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
    if dietary_needs == "" and meal_type != "":
        query = "SELECT * FROM restaurants WHERE name LIKE %s AND meal_type = %s"
        cursor.execute(query, (f'%{search_query}%', meal_type))

    elif search_query != "" and meal_type != "" and meal_type != "":
        query = "SELECT * FROM restaurants WHERE name LIKE %s"
        cursor.execute(query, (f'%{search_query}%'))

    elif dietary_needs != "" and meal_type == "":
        query = "SELECT * FROM restaurants WHERE name LIKE %s AND dietary_needs = %s"
        cursor.execute(query, (f'%{search_query}%', dietary_needs))

    elif dietary_needs == "" and meal_type == "" and search_query == "":
        query = "SELECT * FROM restaurants"
        cursor.execute(query)
    else:
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
            'image': row['image'],
            'rating': row['rating'],
            'numberofrating': row['numberofrating']
            # Add more fields as needed
        }
        restaurant_data.append(restaurant_info)

    # Close the cursor and MySQL connection
    cursor.close()
    return render_template('restaurants_view.html', restaurant_data=restaurant_data)

@app.route("/allrestaurants", methods=['GET'])
def restaurants_view():
    # Get the rating_order query parameter from the URL
    rating_order = request.args.get('rating_order')
    min_ratings = request.args.get('min_ratings')
    
    # Create a cursor for executing SQL queries
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Create a list to store restaurant data
    restaurant_data = []

    # Build and execute the SQL query
    query = "SELECT * FROM restaurants"
    
    if min_ratings:
        query += f" WHERE numberofrating >= {min_ratings}"
    
    if rating_order == 'high_to_low':
        query += " ORDER BY rating DESC"
    elif rating_order == 'low_to_high':
        query += " ORDER BY rating ASC"
    
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
            'image': row['image'],
            'rating': row['rating'],
            'numberofrating': row['numberofrating']
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


# @app.route("/form", methods=['POST'])
# def particulars_form():
#     if request.method == "POST":
#         name = request.form['name']
#         phone = request.form['phone']
#         email = request.form['email']
#         timing = request.form['timing']
#         size = request.form['size']

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("INSERT INTO particulars (name, phone, email, size, timing) VALUES (%s, %s, %s, %s, %s)", (name, phone, email, size, timing))
#         cursor.connection.commit()
#         cursor.close()

#         # Save the form data in a dictionary
#         form_data = {
#             'name': name,
#             'phone': phone,
#             'email': email,
#             'timing': timing,
#             'size': size,
#         }

#         # Assuming you have a success.html template
#         return render_template('success.html', form_data=form_data)

#     # Handle GET requests or other cases
#     return render_template('error.html')  # You can create an error.html template for error cases

@app.route("/form", methods=['POST'])
def make_booking():
    if request.method == "POST":

        # Extract data from the request
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        timing = request.form['timing']
        size = int(request.form['size'])

        # Create a gRPC channel to the server
        channel = grpc.insecure_channel('localhost:50051')  # Replace with your server's address

        # Create a stub for the BookingService
        stub = booking_pb2_grpc.BookingServiceStub(channel)

        # Create a BookingRequest message
        booking_request = booking_pb2.BookingRequest(
            name=name,
            phoneNumber=phone,
            email=email,
            timing=timing,
            size=size
        )

        # Call the gRPC client function
        response = stub.Booking(booking_request)

        # Save the form data in a dictionary
        form_data = {
            'name': response.name,
            'phone': response.phone,
            'email': response.email,
            'timing': response.timing,
            'size': response.size,
        }

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO particulars (name, phone, email, size, timing) VALUES (%s, %s, %s, %s, %s)", (name, phone, email, size, timing))
        cursor.connection.commit()
        cursor.close()

        # Assuming you have a success.html template
        return render_template('success.html', form_data=form_data)

    # Handle GET requests or other cases
    return render_template('error.html')  # You can create an error.html template for error cases

if __name__ == '__main__':
    # app.run(debug=True)
    # make it accessible from your host machine when dockerising the app 
    app.run(host='0.0.0.0', port=5000)
