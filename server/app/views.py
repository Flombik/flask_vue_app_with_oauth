from flask import request

from server.app import app
from .models import Book, Author, Genre, PublishHouse, db


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
def add_book():
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

        return {'status': 'success', 'message': 'Book added!'}


@app.route("/books/<int:book_id>/edit/", methods=['put'])
def edit_book(book_id):
    if request.method == 'PUT':
        data = request.get_json()
        title = data.get('title')
        author_name = data.get('author')
        genre_name = data.get('genre')
        year = data.get('year')
        pages = data.get('pages')
        publish_house_name = data.get('publisher')

        book = db.session.query(Book).filter(Book.id == book_id).one()

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
def delete_book(book_id):
    if request.method == 'DELETE':
        book = db.session.query(Book).filter(Book.id == book_id).one()
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
def add_author():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        direction = data.get('direction')
        dom = data.get('date_of_birth')

        author = Author()

        author.name = name
        author.date_of_birth = dom
        author.direction = direction

        db.session.add(author)
        db.session.commit()

        return {'status': 'success', 'message': 'Author added!'}


@app.route('/authors/<int:author_id>/edit/', methods=['put'])
def edit_author(author_id):
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        direction = data.get('direction')
        dom = data.get('date_of_birth')

        author = db.session.query(Author).filter(Author.id == author_id).one()

        author.name = name
        author.date_of_birth = dom
        author.direction = direction

        db.session.add(author)
        db.session.commit()

        return {'status': 'success', 'message': 'Author updated!'}


@app.route('/authors/<int:author_id>/delete/', methods=['delete'])
def delete_author(author_id):
    if request.method == 'DELETE':
        author = db.session.query(Author).filter(Author.id == author_id).one()
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
def add_publisher():
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
        db.session.add(publisher)
        db.session.commit()

        return {'status': 'success', 'message': 'Publisher added!'}


@app.route('/publishers/<int:publisher_id>/edit/', methods=['put'])
def edit_publisher(publisher_id):
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        address = data.get('address')
        phone_num = data.get('phone_num')
        website = data.get('website')

        publisher = db.session.query(PublishHouse).filter(PublishHouse.id == publisher_id).one()

        publisher.name = name
        publisher.address = address
        publisher.phone_num = phone_num
        publisher.website = website
        db.session.add(publisher)
        db.session.commit()

        return {'status': 'success', 'message': 'Publisher updated!'}


@app.route('/publishers/<int:publisher_id>/delete/', methods=['delete'])
def delete_publisher(publisher_id):
    if request.method == 'DELETE':
        publisher = db.session.query(PublishHouse).filter(PublishHouse.id == publisher_id).one()
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
def add_genre():
    if request.method == 'POST':
        data = request.get_json()
        genre_data = data.get('genre')

        genre = Genre()

        genre.genre = genre_data

        db.session.add(genre)
        db.session.commit()

        return {'status': 'success', 'message': 'Genre added!'}


@app.route('/genres/<int:genre_id>/delete/', methods=['delete'])
def delete_genre(genre_id):
    if request.method == 'DELETE':
        genre = db.session.query(Genre).filter(Genre.id == genre_id).one()
        db.session.delete(genre)
        db.session.commit()
        return {'status': 'success', 'message': 'Genre deleted!'}


def if_exist(obj):
    return obj if obj else None
