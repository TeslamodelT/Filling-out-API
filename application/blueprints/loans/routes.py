from .schemas import loan_schema, loans_schema
from flask import request, jsonify
from marshmallow import ValidationError 
from sqlalchemy import select 
from application.models import Loan, Book, db
from . import loans_bp
from application.blueprints.books.schemas import books_schema

@loans_bp.route("/", methods=['POST'])
def create_loan():
    try:
        loan_data = loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_loan = Loan(**loan_data)
    db.session.add(new_loan)
    db.session.commit()
    return loan_schema.jsonify(new_loan), 201

#GET ALL LOANS
@loans_bp.route("/", methods=['GET'])
def get_loans():
    query = select(Loan)
    loans = db.session.execute(query).scalars().all()
    
    return loans_schema.jsonify(loans)

#GET SPECIFIC LOAN
@loans_bp.route("/<int:loan_id>", methods=['GET'])
def get_loan(loan_id):
    loan = db.session.get(Loan, loan_id)

    if loan:
        return loan_schema.jsonify(loan), 200
    return jsonify({"error": "loan not found."}), 404

#ADD BOOK TO LOAN
@loans_bp.route("/<int:loan_id>/add-book/<int:book_id>", methods=['PUT'])
def add_book(loan_id,book_id):
    loan = db.session.get(Loan, loan_id)
    book = db.session.get(Book, book_id)
    
    if loan and book:
        if book not in loan.books:
            loan.books.append(book)
            db.session.commit()
            return jsonify({
                "message": "successfully added book to loan",
                "loan": loan_schema.dump(loan),
                "books": books_schema.dump(loan.books)
            }), 200
        return jsonify({"error": "This book is already included on this loan."}), 400
    return jsonify({"error": "Invalid book_id or loan_id"}), 400

#REMOVE BOOK FROM LOAN
@loans_bp.route("/<int:loan_id>/remove-book/<int:book_id>", methods=['PUT'])
def remove_book(loan_id,book_id):
    loan = db.session.get(Loan, loan_id)
    book = db.session.get(Book, book_id)
    
    if loan and book:
        if book in loan.books:
            loan.books.remove(book)
            db.session.commit()
            return jsonify({
                "message": "successfully removed book to loan",
                "loan": loan_schema.jsonify(loan),
                "books": books_schema.jsonify(loan.books)
            }), 200
        return jsonify({"error": "This book is not included on this loan."}), 400
    return jsonify({"error": "Invalid book_id or loan_id"}), 400

#DELETE SPECIFIC LOAN
@loans_bp.route("/<int:loan_id>", methods=['DELETE'])
def delete_loan(loan_id):
    loan = db.session.get(Loan, loan_id)

    if not loan:
        return jsonify({"error": "Loan not found."}), 404
    
    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": f'Loan id: {loan_id}, successfully deleted.'}), 200