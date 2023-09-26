from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/restaurant/abc") #replace abc dynamically, restaurant remains static
def restaurant_profile():
    return render_template('restaurant_profile.html')

if __name__ == '__main__':
    app.run(debug=True)