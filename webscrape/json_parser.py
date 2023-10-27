import json
import pymysql
import boto3

def bring_data_over_mysql():
    connection = pymysql.connect(
        host='aws-cloud-db.c51u88x7edpw.us-east-1.rds.amazonaws.com',
        user='admin',
        password='pmB6YW7fYDuRo0Be8sEJ',
        db='clouddb2'
    )
    cursor = connection.cursor()

    with open('restaurant_data.json', 'r') as json_file:
        data = json.load(json_file)

        for item in data:
            query = "INSERT INTO restaurant_data (name, location, imageLink, rating) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (item['name'], item['location'], item['imageLink'], item['rating']))
        
    connection.commit()
    connection.close()