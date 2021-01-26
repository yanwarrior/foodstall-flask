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

