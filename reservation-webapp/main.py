from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/restaurants")
def restaurants_list():
    return render_template('restaurant_list.html')

@app.route("/restaurant/abc") #replace abc dynamically, restaurant remains static
def restaurant_profile():
    return render_template('restaurant_profile.html')

@app.route("/form")
def particulars_form():
    return render_template('particulars_form.html')

if __name__ == '__main__':
    app.run(debug=True)