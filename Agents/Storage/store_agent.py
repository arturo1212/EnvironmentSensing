import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime

def createReadTable(conn):
    #Connecting to sqlite

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS ENV_READ")

    #Creating table as per requirement
    sql ='''CREATE TABLE ENV_READ(
        ID TEXT NOT NULL,
        TEMPERATURE FLOAT,
        HUMIDITY FLOAT,
        RECPT_DT TEXT
    )'''
    cursor.execute(sql)
    print("Table created successfully........")

    # Commit your changes in the database
    conn.commit()

def insertVaribleIntoTable(sqliteConnection, id, name, email, joinDate):
    try:
        cursor = sqliteConnection.cursor()
        sqlite_insert_with_param = """INSERT INTO ENV_READ
                          (id, temperature, humidity, recpt_dt) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (id, name, email, joinDate)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into ENV_READ table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    client.subscribe("sensor/humidity")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))
    
    # Store received message
    parsed_msg = str(msg.payload).split(",")
    conn = sqlite3.connect('../../demoenv.db')
    insertVaribleIntoTable(conn, parsed_msg[0][2:], parsed_msg[1], parsed_msg[2], datetime.now().isoformat()) # parsed_msg[0][2:]
    conn.close()

"""
conn = sqlite3.connect('demoenv.db')
createReadTable(conn)
conn.close()
"""

if __name__ == "__main__":
    client = mqtt.Client("store_agent")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.0.2", 1883, 60)
    client.loop_forever()


#insertVaribleIntoTable(conn, 1.0, 2.0, 3.0, "2019-05-19")
