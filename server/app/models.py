from server.app import db

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    year_of_writing = db.Column(db.String(255))
    pages = db.Column(db.String(255))
    publish_house_id = db.Column(db.Integer, db.ForeignKey('publish_houses.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.title


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    direction = db.Column(db.String(255))
    date_of_birth = db.Column(db.String(255))
    books = db.relationship('Book', backref='author')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.name


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(255), nullable=False, unique=True)
    books = db.relationship('Book', backref='genre')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.genre


class PublishHouse(db.Model):
    __tablename__ = 'publish_houses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255))
    phone_num = db.Column(db.String(20))
    website = db.Column(db.String(255))
    books = db.relationship('Book', backref='publish_house')
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return self.name


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    books = db.relationship('Book', backref='creator')
    authors = db.relationship('Author', backref='creator')
    genres = db.relationship('Genre', backref='creator')
    publishers = db.relationship('PublishHouse', backref='creator')

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return None

        return user
