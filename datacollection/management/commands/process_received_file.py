
from django.core.management.base import BaseCommand, CommandError
from datacollection.views import read_file
class Command(BaseCommand):
    help = """
        Processes the file found in the folder received_files
    """

    def handle(self, *args, **options):
        try:
            process_result = read_file()
            print(process_result)
        except Exception as error:
            print('Exception when reading file', error)
