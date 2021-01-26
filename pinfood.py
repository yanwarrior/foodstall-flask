import json

from werkzeug.utils import redirect

from dbhelper import DBHelper
from googleapi import google_script_src
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    foods = DB.get_all_foods()
    foods = json.dumps(foods)
    return render_template("home.html",
                           foods=foods,
                           google_script_src=google_script_src)


@app.route("/save-food", methods=['POST'])
def save_food():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")

    DB.add_food(category,
                date,
                latitude,
                longitude,
                description)

    return redirect('/')


if __name__ == '__main__':
    app.run(port=5000, debug=True)