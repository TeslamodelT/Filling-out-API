import unittest
from datetime import date, datetime
from app import create_app, db
from application.models import Member, Order

class TestOrder(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.member = Member(
            name="test_user",
            email="test@email.com",
            DOB=datetime.strptime("1900-01-01", "%Y-%m-%d").date(),
            password='test'
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.member)
            db.session.commit()
        self.client = self.app.test_client()

        self.order_data = {
            "order_date": "2025-09-30",
            "member_id": self.member.id
        }

    def test_create_order(self):
        response = self.client.post('/orders/', json=self.order_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['member_id'], self.member.id)

    def test_invalid_order_creation(self):
        incomplete_data = {
            "order_date": "2025-09-30"
        }

        response = self.client.post('/orders/', json=incomplete_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('member_id', response.json)

    def test_get_all_orders(self):
        with self.app.app_context():
            order = Order(order_date=date.today(), member_id=self.member.id)
            db.session.add(order)
            db.session.commit()

        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['member_id'], self.member.id)

    def test_delete_order(self):
        with self.app.app_context():
            order = Order(order_date=date.today(), member_id=self.member.id)
            db.session.add(order)
            db.session.commit()
            order_id = order.id

        response = self.client.delete(f'/orders/{order_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Order deleted successfully')

