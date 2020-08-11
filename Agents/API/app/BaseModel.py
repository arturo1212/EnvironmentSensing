
from sqlalchemy import desc
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

database_path = "sqlite:///demoenv.db"
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String, primary_key=True)
    full_name = db.Column(db.String, nullable=False, default="No name")
    profile = db.Column(db.String, default="guest")
    img_url = db.Column(db.String, default="default.png")
    agents = relationship("Agent", secondary=lambda: agent_user_association.__table__)

# Agent and Events
class Agent(db.Model):
    __tablename__ = 'agent'
    mac_address = db.Column(db.String, primary_key=True)
    alias = db.Column(db.String, nullable=False, default="No Alias")
    users = relationship("User", secondary=lambda: agent_user_association.__table__)
    events = relationship("AgentEvent", backref="agent", lazy="dynamic")
    reads = relationship("EnvironmentRead", backref="agent", lazy="dynamic")

class agent_user_association(db.Model):
    __tablename__ = 'agent_user_association'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, db.ForeignKey('user.email'))
    mac_address = db.Column(db.String, db.ForeignKey('agent.mac_address'))
    user = relationship(User, backref=backref("agent_user_association", cascade="all, delete-orphan"))
    agent = relationship(Agent, backref=backref("agent_user_association", cascade="all, delete-orphan"))

class AgentEvent(db.Model):
    __tablename__ = 'agent_event'
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    status = db.Column(db.String, default="Created")
    description = db.Column(db.String, default="No Description Available")
    created_dt = db.Column(db.DateTime, default=datetime.utcnow)
    mac_address = db.Column(db.String, db.ForeignKey('agent.mac_address'))

# Reads
class EnvironmentRead(db.Model):
    __tablename__ = 'env_read'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mac_address = db.Column(db.String, db.ForeignKey('agent.mac_address'))
    temperature = db.Column(db.Integer, default = 0)
    humidity = db.Column(db.Integer, default = 0)
    moisture = db.Column(db.Integer, default = 0)
    read_dt = db.Column(db.DateTime, default=datetime.utcnow)