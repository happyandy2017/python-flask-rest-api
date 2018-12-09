from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique= True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return str({
            'username': self.name,
            'password': self.password
        })
    
    def username_password_match(_usernmae, _password):
        user = User.query.filter_by(name=_usernmae).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True

    def getAllUsers():
        return User.query.all()

    def createUser(_username, _password):
        new_user = User(name=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()
