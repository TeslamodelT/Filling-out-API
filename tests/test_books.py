import unittest
from flask_app import create_app, db
from application.models import Book

class TestBook(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

        self.book_data = {
            "author": "Jane Austen",
            "genre": "Fiction",
            "desc": "A classic novel of manners.",
            "title": "Pride and Prejudice"
        }

    def test_create_book(self):
        response = self.client.post('/books/', json=self.book_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], "Pride and Prejudice")

    def test_invalid_book_creation(self):
        incomplete_data = {
            "author": "Jane Austen",
            "genre": "Fiction",
            "desc": "Missing title field"
        }

        response = self.client.post('/books/', json=incomplete_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.json)

    def test_get_all_books(self):
        with self.app.app_context():
            book = Book(**self.book_data)
            db.session.add(book)
            db.session.commit()

        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['title'], "Pride and Prejudice")

    def test_delete_book(self):
        with self.app.app_context():
            book = Book(**self.book_data)
            db.session.add(book)
            db.session.commit()
            book_id = book.id

        response = self.client.delete(f'/books/{book_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Book deleted successfully')

