import os, datetime
import pandas as pandas
from django.http import JsonResponse

from django.core.mail import EmailMessage
from lawrence_data_aggregation import settings

from .models import Region, Country, Project, Loan
from datacollection.data_aggregation import AggregationHandler

# Create your views here.

def read_file():
    return DataCompile().read_file()
    
def data_collection(request):
    summary = DurationSummaryHandler(request.GET.get('from'), request.GET.get('to')).get_summary()
    return JsonResponse({'results': summary,'message': 'processed'})
    

class DataCompile:
    def read_file(self):
        """
        Reads the file received.
        Saves the records into the database
        """
        module_dir = os.path.dirname(__file__)  
        file_path = os.path.join(module_dir, '../received_files/dataset.csv')   #full path to text.
        dataset = pandas.read_csv(file_path)

        # the processed file path
        today = datetime.datetime.now().date()
        processed_file_name = '../processed_files/processed'+str(today)+'.csv'
        processed_file_path = os.path.join(module_dir, processed_file_name)        

        # get the column names of the file
        # formulate the column names to remove spaces and some unwanted characters
        dataset_columns = []
        for column in dataset.columns:
            # remove the spaces
            header = column.replace(" ", "_").lower()
            # remove the 's
            header = header.replace("'s", "")
            # remove the (
            header = header.replace("(", "")
            # remove the )
            header = header.replace(")", "")
            # remove the trailing space at the end of the string
            str_len = len(header)
            if (header[str_len-1]) == '_':
                header = header[:str_len-1]
            
            dataset_columns.append(header)
        
        dataset.columns = dataset_columns

        summary = AggregationHandler(dataset).aggregate()
        
        try:
            return summary
        finally:
            # create a bulk insert object to save to the database after the proce
            bulk_insert_records = []
            for record in dataset.itertuples():            
                bulk_insert_records.append(LoanHandler(record).formulate_loan_object())
                # if record.Index > 20:
                #     break

            # bulk insert into the database
            LoanHandler(bulk_insert_records).save()

            # move the file to a new directory
            os.rename(file_path, processed_file_path)

            # send the email notification
            message_body = summary
            NotificationHandler(summary).send_email_notification()


class DurationSummaryHandler:
    def __init__(self, date_from, date_to):
        self.df = date_from
        self.dt = date_to

    def get_summary(self):
        loans = Loan.objects.filter(
            end_of_period__gte = self.df,
            end_of_period__lte = self.dt
        ).values('interest_rate',
            'original_principal_amount', 
            'cancelled_amount', 
            'undisbursed_amount', 
            'disbursed_amount', 
            'repaid_to_ibrd', 
            'due_to_ibrd', 
            'exchange_adjustment', 
            'borrower_obligation', 
            'sold_3rd_party', 
            'repaid_3rd_party', 
            'due_3rd_party', 
            'loans_held')
        dataset = pandas.DataFrame(list(loans))
        return AggregationHandler(dataset).aggregate()


class RegionHandler:
    """
    Handles model writes and reads for REGIONS
    """
    def __init__(self, region_name):
        self.region = region_name.upper()

    def save(self):
        """
        Saves the region to the db
        """
        try:
            region = Region(region=self.region).save()
            return region
        except Exception as error:
            print('ERegionHandlerSave', error)
            return False

    def get_region_id(self):
        """
        Saves the region in case it has not been saved before.
        Returns the region object
        """
        try:
            region = Region.objects.get(region=self.region)
            return region
        except:
            return self.save()


class CountryHandler:
    def __init__(self, country_code, country_name):
        self.country_code = str(country_code).upper()
        self.country_name = str(country_name).upper()

    def save(self):
        try:
            country = Country(
                country_code = self.country_code,
                country = self.country_name
                )
            country.save()
            return country
        except Exception as error:
            print('ECountryHandlerSave', error)

    def get_country_id(self):
        try:
            country = Country.objects.get(country = self.country_name)
            return country
        except:
            return self.save()
       
    
class ProjectHandler:
    def __init__(self, project_id, project_name):
        self.project_id = str(project_id).upper()
        self.project_name = str(project_name).upper()

    def save(self):
        try:
            project = Project(
                project_id = self.project_id,
                project_name = self.project_name
                ).save()
            return project
        except Exception as error:
            print('EProjectHandlerSave', error)
            return False

    def get_project_id(self):
        try:
            project = Project.objects.get(project_id = self.project_id)
            return project
        except:
            return self.save()


class LoanHandler:
    def __init__(self, loan_object):
        self.loan = loan_object


    def formulate_loan_object(self):
        loan = Loan(
            end_of_period = self.loan.end_of_period,
            loan_number = self.loan.loan_number,
            region = RegionHandler(self.loan.region).get_region_id(),
            country_code = CountryHandler(self.loan.country_code, self.loan.country).get_country_id(),
            borrower = self.loan.borrower,
            guarantor = self.loan.guarantor,
            guarantor_country_code = CountryHandler(self.loan.guarantor_country_code, self.loan.guarantor_country_code).get_country_id(),
            loan_type = self.loan.loan_type,
            loan_status = self.loan.loan_status,
            interest_rate = self.loan.interest_rate,
            currency_of_commitment = self.loan.currency_of_commitment,
            project = ProjectHandler(self.loan.project_id, self.loan.project_name).get_project_id(),
            original_principal_amount = self.loan.original_principal_amount,
            cancelled_amount = self.loan.cancelled_amount,
            undisbursed_amount = self.loan.undisbursed_amount,
            disbursed_amount = self.loan.disbursed_amount,
            repaid_to_ibrd= self.loan.repaid_to_ibrd,
            due_to_ibrd = self.loan.due_to_ibrd,
            exchange_adjustment = self.loan.exchange_adjustment,
            borrower_obligation = self.loan.borrower_obligation, 
            sold_3rd_party = self.loan.sold_3rd_party,
            repaid_3rd_party = self.loan.repaid_3rd_party,
            due_3rd_party = self.loan.due_3rd_party,
            loans_held = self.loan.loans_held,
            first_repayment_date = self.loan.first_repayment_date,
            last_repayment_date = self.loan.last_repayment_date,
            agreement_signing_date = self.loan.agreement_signing_date,
            board_approval_date = self.loan.board_approval_date,
            effective_date_most_recent = self.loan.effective_date_most_recent,
            closed_date_most_recent = self.loan.closed_date_most_recent,
            last_disbursement_date = self.loan.last_disbursement_date    
        )
        return loan

    def save(self):
        Loan.objects.bulk_create(self.loan)


class NotificationHandler:
    def __init__(self, message_body):
        self.message_body = message_body

    def send_email_notification(self):
		# with transaction.atomic():
        subject = "File load update"
        to = [''+settings.EMAIL_HOST_USER]
        from_email = ''+settings.EMAIL_HOST_USER		
        message = "<html><center>The summary is as follows</center>"+str(self.message_body)+"</html>"	
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send(fail_silently=False)
        