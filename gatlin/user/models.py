from gatlin.extensions import db, cache
from datetime import datetime
from flask.ext.login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash




class Base(object):

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def all(self):
        return db.query(self).all()


class User(db.Model,UserMixin,Base):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(200),unique=True)
    password = db.Column(db.String(120), nullable=False)
    joined = db.Column(db.DateTime, default=datetime.utcnow())
    lastseen = db.Column(db.DateTime, default=datetime.utcnow())
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(10))
    website = db.Column(db.String(200))
    location = db.Column(db.String(100))
    avatar = db.Column(db.String(200))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def set_password(self, raw_password):
        """Generates a password hash for the provided password"""
        self.password = generate_password_hash(raw_password)


    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false"""

        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, login, password):
        """A classmethod for authenticating users
        It returns true if the user exists and has entered a correct password

        :param login: This can be either a username or a email address.

        :param password: The password that is connected to username and email.
        """

        user = cls.query.filter(User.username == login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated


class Connect(db.Model):
    __tablename__ = "connects"

    id = db.Column(db.Integer, primary_key=True)
    connecter = db.Column(db.Integer)
    connected = db.Column(db.Integer)
    status = db.Column(db.String(200))



