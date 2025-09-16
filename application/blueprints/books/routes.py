from .schemas import book_schema, books_schema
from flask import request, jsonify
from marshmallow import ValidationError 
from sqlalchemy import select 
from application.models import Book, db
from . import books_bp

@books_bp.route("/", methods=['POST'])
def create_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_book = Book(**book_data)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book), 201

#GET ALL BOOKS
@books_bp.route("/", methods=['GET'])
def get_books():
    query = select(Book)
    books = db.session.execute(query).scalars().all()
    
    return books_schema.jsonify(books)

#GET SPECIFIC BOOK
@books_bp.route("/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = db.session.get(Book, book_id)

    if book:
        return book_schema.jsonify(book), 200
    return jsonify({"error": "book not found."}), 404

#UPDATE SPECIFIC BOOK
@books_bp.route("/<int:book_id>", methods=['PUT'])
def update_book(book_id):
    book = db.session.get(Book, book_id)

    if not book:
        return jsonify({"error": "Book not found."}), 404
    
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in book_data.items():
        setattr(book, key, value)

    db.session.commit()
    return book_schema.jsonify(book), 200

#DELETE SPECIFIC BOOK
@books_bp.route("/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if not book:
        return jsonify({"error": "Book not found."}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f'Book id: {book_id}, successfully deleted.'}), 200