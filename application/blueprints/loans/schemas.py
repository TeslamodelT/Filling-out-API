from application.extensions import ma
from application.models import Loan

class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loan

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)