from flask_login import UserMixin

from app.orm.db import db

user_role = db.Table('user_role',
                     db.Column('uid', db.String(36), db.ForeignKey('user.uid')),
                     db.Column('rid', db.String(36), db.ForeignKey('role.rid')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    uid = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45))
    telephone = db.Column(db.String(45))
    email = db.Column(db.String(45))

    roles = db.relationship('Role', secondary=user_role,
                            backref=db.backref('users', lazy='dynamic'))

    papers = db.relationship('Paper', backref='user',
                             lazy='dynamic')

    labels = db.relationship('Label', backref='user',
                             lazy='dynamic')

    def get_id(self):
        return self.uid



class Role(db.Model):
    __tablename__ = 'role'

    rid = db.Column(db.String(36), primary_key=True)
    rolename = db.Column(db.String(45), unique=True, nullable=False)


class Paper(db.Model):
    __tablename__ = 'paper'

    pid = db.Column(db.String(36), primary_key=True)
    uid = db.Column(db.String(36), db.ForeignKey('user.uid'))
    title = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.String(2000))
    year = db.Column(db.Integer)
    conference = db.Column(db.String(200))
    url = db.Column(db.String(200))
    time = db.Column(db.DateTime)


class Label(db.Model):
    __tablename__ = 'label'

    lid = db.Column(db.String(36), primary_key=True)
    pid = db.Column(db.String(36), db.ForeignKey('paper.pid'))
    uid = db.Column(db.String(36), db.ForeignKey('user.uid'))
    info = db.Column(db.String(2000), nullable=False)
    time = db.Column(db.DateTime)


class Score(db.Model):
    __tablename__ = 'score'

    sid = db.Column(db.String(36), primary_key=True)
    lid = db.Column(db.String(36), db.ForeignKey('label.lid'))
    uid = db.Column(db.String(36), db.ForeignKey('user.uid'))
    s = db.Column(db.Integer)


class ConferenceDict(db.Model):
    __tablename__ = 'conference_dict'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(500), unique=True)
