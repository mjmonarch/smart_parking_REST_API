from email.policy import default
from unittest.mock import DEFAULT
import psycopg2
from psycopg2 import sql

DBNAME = 'pi'
USER = 'pi'
PASSWORD = '$ecretP2nda'
HOST = '192.168.0.112'
PORT = 5432

connection = psycopg2.connect(dbname=DBNAME, user=USER,
                        password=PASSWORD, host=HOST, port=PORT)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS facts")
query = """
        CREATE TABLE facts(_id serial primary key, date DATE, time TIME, 
        violationType TEXT,car_vrp TEXT, car_contour INTEGER, violation BOOLEAN, 
        locationLatitude REAL, locationLongitude REAL, photoContent BYTEA, id TEXT, 
        dispatchCode INTEGER, zoneNumber INTEGER, country TEXT NULL, address TEXT NULL, 
        city TEXT NULL)
        """
cursor.execute(query)

cursor.execute("DROP TABLE IF EXISTS test")
query = """
        CREATE TABLE test(_id serial primary key, num INTEGER)
        """
cursor.execute(query)

query = "INSERT INTO test VALUES(default, %s)"
cursor.execute(query, (17,))

query = "INSERT INTO test VALUES(default, 64)"
cursor.execute(query)

connection.commit()
connection.close()
