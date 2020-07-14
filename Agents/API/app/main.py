# Expose endpoint
import sqlite3, json
from datetime import datetime
import flask
import json
from flask_cors import CORS, cross_origin

active_sensors = ['balcony', 'kitchen']

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('../../demoenv.db')
        sqliteConnection.row_factory = dict_factory
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_select_query = ""
        aux = 0
        sqlite_select_query += """
                SELECT ID, TEMPERATURE, HUMIDITY, datetime(RECPT_DT) as RECPT_DT from ENV_READ
                ORDER BY datetime(RECPT_DT) DESC
                LIMIT 10 
                """
        cursor.execute(sqlite_select_query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        return data
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

readSqliteTable()

@app.route('/sensor_history', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def sensor_history():
    return json.dumps({'result': readSqliteTable()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)