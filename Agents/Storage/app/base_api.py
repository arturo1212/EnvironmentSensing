from flask import Flask, request
from flask_cors import CORS, cross_origin
import flask_restless, json
from BaseModel import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

with app.app_context():
    # Create the Flask-Restless API manager. (/api/{tablename})
    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PATCH'])
    manager.create_api(Agent, methods=['GET', 'POST', 'DELETE', 'PATCH'])

    @app.route('/api/agent_last_status', methods=['GET'])
    @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
    def agent_last_reads():
        # - History: Read And Event List (with limits) for single agent
        num_events = request.args.get('num_events')
        num_reads = request.args.get('num_reads')
        agentid = "A4:CF:12:ED:58:5A" #request.args.get('mac_address')
        agent = Agent.query.filter_by(mac_address=agentid).first()
        events = agent.events.limit(num_events).all()
        reads = agent.reads.limit(num_events).all()
        return json.dumps({"mac_address": agent.mac_address, "reads":[row2dict(r) for r in reads], "events":[row2dict(r) for r in reads] })
        #return  json.dumps([dict(r) for r in result]) 

    def addAgentToUser(user, agent):
        user.agents.append(agent)
        db.session.commit()

    # start the flask loop
    app.run()