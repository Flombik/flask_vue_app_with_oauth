from flask import request, redirect, url_for, jsonify
import urllib.parse as parser
import requests
import jwt
from functools import wraps
from datetime import datetime, timedelta
import webbrowser
import asyncio

from server.app import app
from .models import Book, Author, Genre, PublishHouse, User, db


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 1:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[0]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = db.session.query(User).filter(User.email == data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route('/login/', methods=['post'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    username = user.email.split('@')[0]

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8'), 'username': username})


@app.route('/register/', methods=['post'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return {'status': 'success', 'message': 'Registered successfully!'}


def oauth_login(email):
    query_res = db.session.query(User).filter(User.email == email).first()
    if query_res is None:
        user = User(email)
        db.session.add(user)
        db.session.commit()
    else:
        user = query_res

    username = user.email.split('@')[0]
    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        app.config['SECRET_KEY'])
    return {'token': token.decode('UTF-8'), 'username': username}


@app.route('/login/github/')
def login_via_github():
    authorization_code_req = {'client_id': '4e0a85b77b11c9e13162'}
    authorization_link = 'https://github.com/login/oauth/authorize?{}'.format(parser.urlencode(authorization_code_req))
    return {'status': 'success', 'link': authorization_link}


@app.route('/login/github/callback/')
def github_callback():
    query = request.query_string
    if query != b'':
        query_data = parser.parse_qs(query)
        code = query_data[b'code'][0].decode('utf-8')
        token_req = {
            'client_id': '4e0a85b77b11c9e13162',
            'client_secret': 'c9b5069fc71c51be2657c8960dadea17106b3774',
            'code': code
        }
        token_resp = requests.post('https://github.com/login/oauth/access_token?%s' % parser.urlencode(token_req),
                                   headers={'Accept': 'application/json'})
        token = token_resp.json().get('access_token')

        user_info_resp = requests.get('https://api.github.com/user',
                                      headers={'Authorization': 'token {}'.format(token)})
        email = user_info_resp.json().get('email')
        token = oauth_login(email)
        return redirect('http://localhost:8080/login?{}'.format(parser.urlencode(token)))


@app.route('/login/vk/')
def login_via_vk():
    authorization_code_req = {'client_id': '7371489',
                              'redirect_uri': 'http://localhost:5000/login/vk/callback',
                              'response_type': 'code',
                              'scope': 'email'}
    authorization_link = 'https://oauth.vk.com/authorize?{}'.format(parser.urlencode(authorization_code_req))
    return {'link': authorization_link}


@app.route('/login/vk/callback/')
def vk_callback():
    query = request.query_string
    if query != b'':
        query_data = parser.parse_qs(query)
        code = query_data[b'code'][0].decode('utf-8')
        token_req = {
            'client_id': '7371489',
            'client_secret': 'JyM13YVJ0VIrKvjaARiR',
            'redirect_uri': 'http://localhost:5000/login/vk/callback',
            'code': code
        }
        response = requests.post('https://oauth.vk.com/access_token?%s' % parser.urlencode(token_req),
                                 headers={'Accept': 'application/json'})
        email = response.json().get('email')
        token = oauth_login(email)
        return redirect('http://localhost:8080/login?{}'.format(parser.urlencode(token)))


@app.route('/login/yandex/')
def login_via_yandex():
    authorization_code_req = {'response_type': 'code', 'client_id': '2786de9efc2c4f819c464b3056b946d5',
                              'force_confirm': 'true'}
    authorization_link = 'https://oauth.yandex.ru/authorize?{}'.format(parser.urlencode(authorization_code_req))
    return {'link': authorization_link}


@app.route('/login/yandex/callback/')
def yandex_callback():
    query = request.query_string
    if query != b'':
        query_data = parser.parse_qs(query)
        code = query_data[b'code'][0].decode('utf-8')
        client_id = '2786de9efc2c4f819c464b3056b946d5'
        client_secret = 'a7f7ef10b108464fa35bd11a2c069937'
        data = 'grant_type=authorization_code'
        data += '&code=' + code
        data += '&client_id=' + client_id
        data += '&client_secret=' + client_secret
        token_resp = requests.post(
            'https://oauth.yandex.ru/token', data=data)
        token = token_resp.json().get('access_token')

        user_info_resp = requests.get('https://login.yandex.ru/info?format=json',
                                      headers={'Authorization': 'OAuth {}'.format(token)})

        email = user_info_resp.json().get('default_email')
        token = oauth_login(email)
        return redirect('http://localhost:8080/login?{}'.format(parser.urlencode(token)))


@app.route('/books/')
def books():
    books = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author.name,
            'genre': book.genre.genre if book.genre else None,
            'year': if_exist(book.year_of_writing),
            'pages': if_exist(book.pages),
            'publisher': book.publish_house.name if book.publish_house else None
        } for book in db.session.query(Book).all()]
    return {'status': 'success', 'books': books}


@app.route('/books/add/', methods=['post'])
@token_required
def add_book(current_user):
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        author_name = data.get('author')
        genre_name = data.get('genre')
        year = data.get('year')
        pages = data.get('pages')
        publish_house_name = data.get('publisher')

        book = Book()

        book.title = title
        book.year_of_writing = year
        book.pages = pages

        query_res = db.session.query(Author).filter(Author.name == author_name).first()
        if query_res is None:
            author = Author(name=author_name, creator=current_user)
        else:
            author = query_res
        book.author = author

        if genre_name is not None:
            query_res = db.session.query(Genre).filter(Genre.genre == genre_name).first()
            if query_res is None:
                genre = Genre(genre=genre_name, creator=current_user)
                genre.creator = current_user
            else:
                genre = query_res
            book.genre = genre

        if publish_house_name is not None:
            query_res = db.session.query(PublishHouse).filter(PublishHouse.name == publish_house_name).first()
            if query_res is None:
                publish_house = PublishHouse(name=publish_house_name, creator=current_user)
                publish_house.creator = current_user
            else:
                publish_house = query_res
            book.publish_house = publish_house

        book.creator = current_user
        db.session.add(book)
        db.session.commit()

        return {'status': 'success', 'message': 'Book added!'}


@app.route("/books/<int:book_id>/edit/", methods=['put'])
@token_required
def edit_book(current_user, book_id):
    if request.method == 'PUT':
        book = db.session.query(Book).filter(Book.id == book_id).one()
        if book.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t edit this, because you are not a creator'}

        data = request.get_json()
        title = data.get('title')
        author_name = data.get('author')
        genre_name = data.get('genre')
        year = data.get('year')
        pages = data.get('pages')
        publish_house_name = data.get('publisher')

        book.title = title
        book.year_of_writing = year
        book.pages = pages

        query_res = db.session.query(Author).filter(Author.name == author_name).first()
        if query_res is None:
            author = Author(name=author_name)
        else:
            author = query_res
        book.author = author

        if genre_name is not None:
            query_res = db.session.query(Genre).filter(Genre.genre == genre_name).first()
            if query_res is None:
                genre = Genre(genre=genre_name)
            else:
                genre = query_res
            book.genre = genre

        if publish_house_name is not None:
            query_res = db.session.query(PublishHouse).filter(PublishHouse.name == publish_house_name).first()
            if query_res is None:
                publish_house = PublishHouse(name=publish_house_name)
            else:
                publish_house = query_res
            book.publish_house = publish_house

        db.session.add(book)
        db.session.commit()

        return {'status': 'success', 'message': 'Book updated!'}


@app.route('/books/<int:book_id>/delete/', methods=['delete'])
@token_required
def delete_book(current_user, book_id):
    if request.method == 'DELETE':
        book = db.session.query(Book).filter(Book.id == book_id).one()
        if book.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t delete this, because you are not a creator'}
        db.session.delete(book)
        db.session.commit()
        return {'status': 'success', 'message': 'Book removed!'}


@app.route('/authors/')
def show_authors():
    authors = [
        {
            'id': author.id,
            'name': author.name if author.name else None,
            'direction': author.direction if author.direction else None,
            'date_of_birth': author.date_of_birth if author.date_of_birth else None

        }
        for author in db.session.query(Author).all()]
    return {'status': 'success', 'authors': authors}


@app.route('/authors/add/', methods=['post'])
@token_required
def add_author(current_user):
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        direction = data.get('direction')
        dom = data.get('date_of_birth')

        author = Author()

        author.name = name
        author.date_of_birth = dom
        author.direction = direction
        author.creator = current_user

        db.session.add(author)
        db.session.commit()

        return {'status': 'success', 'message': 'Author added!'}


@app.route('/authors/<int:author_id>/edit/', methods=['put'])
@token_required
def edit_author(current_user, author_id):
    if request.method == 'PUT':
        author = db.session.query(Author).filter(Author.id == author_id).one()
        if author.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t edit this, because you are not a creator'}

        data = request.get_json()
        name = data.get('name')
        direction = data.get('direction')
        dom = data.get('date_of_birth')

        author.name = name
        author.date_of_birth = dom
        author.direction = direction

        db.session.add(author)
        db.session.commit()

        return {'status': 'success', 'message': 'Author updated!'}


@app.route('/authors/<int:author_id>/delete/', methods=['delete'])
@token_required
def delete_author(current_user, author_id):
    if request.method == 'DELETE':
        author = db.session.query(Author).filter(Author.id == author_id).one()
        if author.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t delete this, because you are not a creator'}
        if len(author.books) == 0:
            db.session.delete(author)
            db.session.commit()
            return {'status': 'success', 'message': 'Author removed!'}
        return {'status': 'fail', 'message': 'Author is NOT removed! Delete all books by this author before this.'}


@app.route('/publishers/')
def show_publishers():
    publishers = [
        {
            'id': publisher.id,
            'name': if_exist(publisher.name),
            'address': if_exist(publisher.address),
            'phone_num': if_exist(publisher.phone_num),
            'website': if_exist(publisher.website)
        }
        for publisher in db.session.query(PublishHouse).all()]
    return {'status': 'success', 'publishers': publishers}


@app.route('/publishers/add/', methods=['post'])
@token_required
def add_publisher(current_user):
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        phone_num = data.get('phone_num')
        website = data.get('website')

        publisher = PublishHouse()

        publisher.name = name
        publisher.address = address
        publisher.phone_num = phone_num
        publisher.website = website
        publisher.creator = current_user

        db.session.add(publisher)
        db.session.commit()

        return {'status': 'success', 'message': 'Publisher added!'}


@app.route('/publishers/<int:publisher_id>/edit/', methods=['put'])
@token_required
def edit_publisher(current_user, publisher_id):
    if request.method == 'PUT':
        publisher = db.session.query(PublishHouse).filter(PublishHouse.id == publisher_id).one()
        if publisher.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t edit this, because you are not a creator'}

        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        phone_num = data.get('phone_num')
        website = data.get('website')

        publisher.name = name
        publisher.address = address
        publisher.phone_num = phone_num
        publisher.website = website
        db.session.add(publisher)
        db.session.commit()

        return {'status': 'success', 'message': 'Publisher updated!'}


@app.route('/publishers/<int:publisher_id>/delete/', methods=['delete'])
@token_required
def delete_publisher(current_user, publisher_id):
    if request.method == 'DELETE':
        publisher = db.session.query(PublishHouse).filter(PublishHouse.id == publisher_id).one()
        if publisher.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t delete this, because you are not a creator'}
        db.session.delete(publisher)
        db.session.commit()
        return {'status': 'success', 'message': 'Publisher deleted!'}


@app.route('/genres/')
def show_genres():
    genres = [
        {
            'id': genre.id,
            'genre': if_exist(genre.genre)
        } for genre in db.session.query(Genre).all()]
    return {'status': 'success', 'genres': genres}


@app.route('/genres/add/', methods=['post'])
@token_required
def add_genre(current_user):
    if request.method == 'POST':
        data = request.get_json()
        genre_data = data.get('genre')

        genre = Genre()

        genre.genre = genre_data
        genre.creator = current_user

        db.session.add(genre)
        db.session.commit()

        return {'status': 'success', 'message': 'Genre added!'}


@app.route('/genres/<int:genre_id>/delete/', methods=['delete'])
@token_required
def delete_genre(current_user, genre_id):
    if request.method == 'DELETE':
        genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
        if genre.creator_id is not current_user.id:
            return {'status': 'fail', 'message': 'You can\'t delete this, because you are not a creator'}
        db.session.delete(genre)
        db.session.commit()
        return {'status': 'success', 'message': 'Genre deleted!'}


def if_exist(obj):
    return obj if obj else None
