# Instructions for making `FoodStall` applications with `Flask`

Web-based application to mark food stalls visited by users.

## System Requirements

- Python 3.8 (required)
- Windows 10 (optional)
- PyCharm Community Edition (optional)
- MySQL (with PHPMyAdmin)

## Package Dependencies

- Flask
- PyMySQL

## Preparation

Run the following commands:

```
$ mkdir foodstall
$ cd foodstall
$ python -m venv .venv
$ .venv\Scripts\activate.bat
$ pip install flask pymysql
```

Create folders and files like the following inside the project root:

![image-20210127040913094](G:\projects\foodstall\docs\assets\image-20210127040913094.png)

> Download Bootstrap and save `bootstrap.min.css` in the` static / css / `folder.

-----



## Coding

### (1) Coding `dbconf.py`

```python
test = True

dbuser = 'your username'
dbpassword = 'your password'
dbname = 'your db name'
dbhost = 'localhost'
```

### (2) Coding `dbhelper.py`

```python
from datetime import datetime

import pymysql
import dbconf


class DBHelper:

    def connect(self):
        return pymysql.connect(host=dbconf.dbhost,
                               user=dbconf.dbuser,
                               passwd=dbconf.dbpassword,
                               db=dbconf.dbname)

    def get_all_foods(self):
        connection = self.connect()
        try:
            query = "SELECT latitude, " \
                    "longitude, " \
                    "date, " \
                    "category, " \
                    "description FROM foods;"

            with connection.cursor() as cursor:
                cursor.execute(query)

            named_foods = []

            for food in cursor:
                print(food)
                named_food = {
                    'latitude': food[0],
                    'longitude': food[1],
                    'date': datetime.strftime(food[2], "%Y-%m-%d"),
                    'category': food[3],
                    'description': food[4],
                }

                named_foods.append(named_food)

            return named_foods
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def add_food(self, category, date, latitude, longitude, description):
        connection = self.connect()

        try:
            sql = "INSERT INTO foods (" \
                  "category, " \
                  "date, " \
                  "latitude, " \
                  "longitude, " \
                  "description) " \
                  "VALUES (%s, %s, %s, %s, %s)"

            with connection.cursor() as cursor:
                cursor.execute(sql,
                               (category,
                                date,
                                latitude,
                                longitude,
                                description))
                connection.commit()

        except Exception as e:
            print(e)
        finally:
            connection.close()

    def clear_foods(self):
        connection = self.connect()

        try:
            sql = "DELETE FROM foods;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
```

### (3) Coding `dbsetup.py`

```python
import pymysql
import dbconf

connection = pymysql.connect(host=dbconf.dbhost,
                             user=dbconf.dbuser,
                             passwd=dbconf.dbpassword)


try:
    with connection.cursor() as cursor:
        sql = f"CREATE DATABASE IF NOT EXISTS {dbconf.dbname}"
        cursor.execute(sql)

        sql = f"""CREATE TABLE IF NOT EXISTS {dbconf.dbname}.foods (
            id int NOT NULL AUTO_INCREMENT,
            latitude FLOAT(10, 6),
            longitude FLOAT(10, 6),
            date DATETIME,
            category VARCHAR(50),
            description VARCHAR(200),
            update_at TIMESTAMP,
            PRIMARY KEY (id)
            );"""

        cursor.execute(sql)

    connection.commit()

finally:
    connection.close()
```

### (4) Coding `googleapi.py`

```python
google_api_key = 'your api key'
google_init_func = 'init'
google_script_src = f'https://maps.googleapis.com/maps/api/js?' \
                    f'key={google_api_key}&' \
                    f'callback={google_init_func}'

```

### (5) Coding `pinfood.py`

```python
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
```

### (6) Coding `templates/home.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Food Stall</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
  <script type="text/javascript" src="{{ google_script_src }}"></script>
  <script>
    var map;
    var marker;
    var lat = -6.190059388922542;
    var long = 106.7599655019272;
    var zoom = 15;
    
    function init() {
        var opt = {
            center: new google.maps.LatLng(lat, long),
            zoom: zoom
        };
    
        map = new google.maps.Map(
            document.getElementById("foodstall-maps"),
            opt
        );
    
        google.maps.event.addListener(map, 'click', function (event) {
            setMarker(event.latLng)
        });
    
        console.log({{ foods | safe }})
        placeFood({{foods | safe}});
    }
    
    function setMarker(location) {
        if (marker) {
            marker.setPosition(location);
        } else {
            marker = new google.maps.Marker({
                position: location,
                map: map
            });
        }
    
        document.getElementById('latitude').value = location.lat();
        document.getElementById('longitude').value = location.lng();
    }
    
    function placeFood(foods) {
        for (i=0; i<foods.length; i++) {
            new google.maps.Marker({
                position: new google.maps.LatLng(
                    foods[i].latitude,
                    foods[i].longitude
                ),
                map: map,
                title: foods[i].date + "\n" + foods[i].category + "\n" + foods[i].description
            });
        }
    }
  </script>
</head>
<body onload="init()">
  <div class="container mt-4 mb-3">
    <div class="row">
      <div class="col-md-12">
        <h1 class="display-4">Food Stall</h1>
      </div>
    </div>
  </div>

  <div class="container mb-3">
    <div class="row">
      <div class="col-md-8">
        <div id="foodstall-maps" style="width: 100%; height: 100%"></div>
      </div>
      <div class="col-md-4">
        <div class="card bg-light">
          <div class="card-body">
            <h4 class="card-title">Submit new Food Stall</h4>
            <form action="/save-food" method="post">
              <div class="form-group">
                <label for="category">Category</label>
                <select class="form-control"
                        name="category" id="category">
                  <option value="eggs">Eggs</option>
                  <option value="fish">Fish</option>
                  <option value="hot-meat">Hot Meat</option>
                  <option value="bread">Bread</option>
                  <option value="preserves">Preserves</option>
                  <option value="beverage">Beverage</option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="date">Date</label>
                <input class="form-control"
                       name="date" id="date" type="date">
              </div>
              
              <div class="form-group">
                <label for="latitude">Latitude</label>
                <input class="form-control"
                       name="latitude" id="latitude" type="text">
              </div>
              
              <div class="form-group">
                <label for="longitude">Longitude</label>
                <input class="form-control"
                       name="longitude" id="longitude" type="text">
              </div>
              
              <div class="form-group">
                <label for="description">Description</label>
                <textarea class="form-control" name="description" id="description"></textarea>
              </div>
              <button class="btn btn-primary" type="submit">
                Submit
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
```

## Running

Setup db (required if the database and table do not already exist):

```
$ python dbsetup.py
```

Then:

```
$ python pinfood.py
```

Open `http://localhost:5000` in a browser:

![image-20210127041742642](G:\projects\foodstall\docs\assets\image-20210127041742642.png)