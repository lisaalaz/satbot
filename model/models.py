# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# # File Name: models.py
# #
# # Creates sql tables for use by flask
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from model import db
import datetime
from sqlalchemy import DateTime


class User(db.Model):  # noqa
    __tablename__ = 'user'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), unique=True)
    # age = db.Column(db.Integer())
    # gender = db.Column(db.String(64))
    # no_anxiety_or_depression_symptoms_shown = db.Column(db.Boolean())
    email = db.Column(db.String(120), unique=True)
    protocols = db.relationship('Protocol', backref='user')
    choices = db.relationship('Choice', backref='user')
    sessions = db.relationship('UserModelSession', backref='user')
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    last_accessed = db.Column(DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Protocol(db.Model):  # noqa
    __tablename__ = 'protocol'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    protocol_chosen = db.Column(db.Integer())
    protocol_was_useful = db.Column(db.String(64))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer(), db.ForeignKey('model_session.id'))
    run_id = db.Column(db.Integer(), db.ForeignKey('model_run.id'))
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)


class Choice(db.Model):  # noqa
    __tablename__ = 'choice'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    choice_desc = db.Column(db.String(120))
    option_chosen = db.Column(db.String(60))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer(), db.ForeignKey('model_session.id'))
    run_id = db.Column(db.Integer(), db.ForeignKey('model_run.id'))
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)


class UserModelRun(db.Model):  # noqa
    __tablename__ = 'model_run'  # noqa
    id = db.Column(db.Integer(), primary_key=True)

    emotion_happy_score = db.Column(db.Integer())
    emotion_sad_score = db.Column(db.Integer())
    emotion_angry_score = db.Column(db.Integer())
    emotion_neutral_score = db.Column(db.Integer())
    emotion_anxious_score = db.Column(db.Integer())
    emotion_scared_score = db.Column(db.Integer())

    antisocial_score = db.Column(db.Integer())
    internal_persecutor_score = db.Column(db.Integer())
    personal_crisis_score = db.Column(db.Integer())
    rigid_thought_score = db.Column(db.Integer())
    session_id = db.Column(db.Integer(), db.ForeignKey('model_session.id'))
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    protocols = db.relationship('Protocol', backref='model_run')


class UserModelSession(db.Model):  # noqa
    __tablename__ = 'model_session'  # noqa
    id = db.Column(db.Integer(), primary_key=True)
    conversation = db.Column(db.Text(), default="")

    protocols = db.relationship('Protocol', backref='model_session')
    choices = db.relationship('Choice', backref='model_session')
    runs = db.relationship("UserModelRun", backref='model_session')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date_created = db.Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = db.Column(DateTime)
