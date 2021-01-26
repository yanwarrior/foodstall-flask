## Food Stall

Web-based application to mark food stalls visited by users.

### Instructions

You can read the instructions [here](./docs/instructions.md)

### Quick Start

Open file `dbconf.py` and fill in the configuration for your database:

```python
test = True

dbuser = 'your username'
dbpassword = 'your password'
dbname = 'your db name'
dbhost = 'localhost'
```

Open file `googleapi.py` and fill in the configuration for your google API key:

```python
google_api_key = 'your api key'
```

And then:

```
$ python dbsetup.py
$ python pinfood.py
```

Open `http://localhost:5000` in a browser.

