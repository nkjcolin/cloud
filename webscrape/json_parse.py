import json
import pymysql

def bring_data_over_mysql():
    #remember to change to details of aws rds
    connection = pymysql.connect(
        host='aws-cloud-db.c51u88x7edpw.us-east-1.rds.amazonaws.com',
        user='admin',
        password='pmB6YW7fYDuRo0Be8sEJ',
        db='clouddb2'
    )
    cursor = connection.cursor()

    with open('restaurant_data_final.json', 'r') as json_file:
        data = json.load(json_file)
        all_reviews =  '['

        for item in data:
            query = "INSERT INTO restaurants (name, location, image, rating, numberofrating, description, timings) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (item['name'], item['location'], item['imageLink'], item['rating'], item['numOfRating'], item['description'], item['timeslot']))

            for review in item['review']:
                all_reviews =  all_reviews + "'" + review + "', "

            all_reviews = all_reviews[:-2] + ']'
            query = "INSERT INTO restaurants (reviews) VALUES (%s)"
            cursor.execute(query, all_reviews)

    connection.commit()
    connection.close()

bring_data_over_mysql()