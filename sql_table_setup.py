import psycopg2

# 17

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
        CREATE TABLE facts(id serial primary key, date DATE, time TIME, 
        violation_type TEXT, car_vrp TEXT, car_contour INTEGER, violation BOOLEAN, 
        location_latitude REAL, location_longitude REAL, photo_content BYTEA, fact_id TEXT, 
        dispatch_code INTEGER, zone_number INTEGER, country TEXT NULL, address TEXT NULL, 
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
