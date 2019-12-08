from django.db import models
import uuid


# Create your models here.
class Region(models.Model):
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = 'regions'


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    class Meta:
        db_table = 'countries'


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_id = models.CharField(max_length=100)
    project_name = models.CharField(max_length=150)
    class Meta:
        db_table = 'projects'


class Loan(models.Model):
    loan_reference = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    end_of_period = models.DateTimeField(auto_now_add=False, null=True)
    loan_number = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    country_code = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='loan_country')
    borrower = models.CharField(max_length=100, null=True)
    guarantor = models.CharField(max_length=100)
    guarantor_country_code = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='loan_guarantor_country')
    loan_type = models.CharField(max_length=100)
    loan_status = models.CharField(max_length=100)
    interest_rate = models.FloatField(null=True)
    currency_of_commitment = models.CharField(max_length=100) 
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    original_principal_amount = models.FloatField(null=True) 
    cancelled_amount = models.FloatField(null=True)
    undisbursed_amount = models.FloatField(null=True)
    disbursed_amount = models.FloatField(null=True)
    repaid_to_ibrd= models.FloatField(null=True)
    due_to_ibrd = models.FloatField(null=True)
    exchange_adjustment = models.FloatField(null=True)
    borrower_obligation = models.FloatField(null=True)
    sold_3rd_party = models.FloatField(null=True)
    repaid_3rd_party = models.FloatField(null=True)
    due_3rd_party = models.FloatField(null=True)
    loans_held = models.FloatField(null=True)
    first_repayment_date = models.CharField(max_length=200, null=True)
    last_repayment_date = models.CharField(max_length=200, null=True)
    agreement_signing_date = models.CharField(max_length=200, null=True)
    board_approval_date = models.CharField(max_length=200, null=True)
    effective_date_most_recent = models.CharField(max_length=200, null=True)
    closed_date_most_recent = models.CharField(max_length=200, null=True)
    last_disbursement_date = models.CharField(max_length=200, null=True)
    class Meta:
        db_table = 'loans'
    

# [
#     'End of Period', 'Loan Number', 'Region', 'Country Code', 'Country', 'Borrower', 
#     'Guarantor Country Code', 'Guarantor', 'Loan Type', 'Loan Status', 'Interest Rate', 
#     'Currency of Commitment', 'Project ID', 'Project Name ', 'Original Principal Amount', 
#     'Cancelled Amount', 'Undisbursed Amount', 'Disbursed Amount', 'Repaid to IBRD', 
#     'Due to IBRD', 'Exchange Adjustment', "Borrower's Obligation", 'Sold 3rd Party', 
#     'Repaid 3rd Party', 'Due 3rd Party', 'Loans Held', 'First Repayment Date', 
#     'Last Repayment Date', 'Agreement Signing Date', 'Board Approval Date', 
#     'Effective Date (Most Recent)', 'Closed Date (Most Recent)', 'Last Disbursement Date'
# ]
