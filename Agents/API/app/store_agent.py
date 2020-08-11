from flask import Flask, request
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from BaseModel import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
db.init_app(app)
with app.app_context():
    def create_env_record(agentid, humidity, temp, moist):
        # Store recorded values
        read = EnvironmentRead(temperature=temp, humidity=humidity, moisture=moist)
        agent = Agent.query.filter_by(mac_address = agentid).first()
        if(agent is None):
            agent = Agent(mac_address=agentid)
            db.session.add(agent)
            db.session.commit()
        agent.reads.append(read)
        db.session.commit()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        #print("Connected with result code " + str(rc))
        client.subscribe("sensor/humidity")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        parsed_msg = str(msg.payload).split(",")
        create_env_record(parsed_msg[0][2:], parsed_msg[1], parsed_msg[2], parsed_msg[3]) # parsed_msg[0][2:]

    if __name__ == "__main__":
        client = mqtt.Client("store_agent")
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("arturothouse.ddns.net", 1883, 60)
        client.loop_forever()


