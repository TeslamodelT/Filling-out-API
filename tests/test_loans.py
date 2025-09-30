import unittest
from datetime import datetime, date
from app import create_app, db
from application.models import Member, Loan

class TestLoan(unittest.TestCase):

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

    def test_create_loan(self):
        loan_payload = {
            "loan_date": "2025-09-30",
            "member_id": self.member.id
        }

        response = self.client.post('/loans/', json=loan_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['member_id'], self.member.id)

    def test_invalid_loan_creation(self):
        loan_payload = {
            "loan_date": "2025-09-30"
        }

        response = self.client.post('/loans/', json=loan_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('member_id', response.json)

    def test_get_all_loans(self):
        with self.app.app_context():
            loan = Loan(loan_date=date.today(), member_id=self.member.id)
            db.session.add(loan)
            db.session.commit()

        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['member_id'], self.member.id)

    def test_delete_loan(self):
        with self.app.app_context():
            loan = Loan(loan_date=date.today(), member_id=self.member.id)
            db.session.add(loan)
            db.session.commit()
            loan_id = loan.id

        response = self.client.delete(f'/loans/{loan_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Loan deleted successfully')

