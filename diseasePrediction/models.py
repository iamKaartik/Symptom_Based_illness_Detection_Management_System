from diseasePrediction import db,login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Users(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False, unique=True)
    email=db.Column(db.String(50), nullable=False, unique=True)
    passwd=db.Column(db.String(20), nullable=False)
    diseases=db.relationship('Diseases',backref='patient',lazy=True)

    def __repr__(self):
        return "User('{}','{}','{}')".format(self.id,self.name,self.email)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Diseases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    date_predicted=db.Column(db.DateTime, default=datetime.now)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return "disease('{}','{}','{}','{}')".format(self.id,self.name, self.date_predicted, self.user_id)