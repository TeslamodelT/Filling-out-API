import unittest
from flask_app import create_app, db
from application.models import Item

class TestItem(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

        self.item_data = {
            "item_name": "Notebook",
            "price": 4.99
        }

    def test_create_item(self):
        response = self.client.post('/items/', json=self.item_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['item_name'], "Notebook")
        self.assertEqual(response.json['price'], 4.99)

    def test_invalid_item_creation(self):
        incomplete_data = {
            "price": 4.99
        }

        response = self.client.post('/items/', json=incomplete_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('item_name', response.json)

    def test_get_all_items(self):
        with self.app.app_context():
            item = Item(**self.item_data)
            db.session.add(item)
            db.session.commit()

        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['item_name'], "Notebook")

    def test_delete_item(self):
        with self.app.app_context():
            item = Item(**self.item_data)
            db.session.add(item)
            db.session.commit()
            item_id = item.id

        response = self.client.delete(f'/items/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Item deleted successfully')

