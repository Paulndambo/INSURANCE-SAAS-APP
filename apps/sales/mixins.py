from apps.sales.queries import query
from django.db import connection
class BulkMembersOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    
    def run(self):
        self.__create_scheme_group()

    
    def __create_scheme_group(self):
        """
        : Create Scheme Group & Policy
        """
        members = self.data
        #for member in members:
        #    member.processed = True
        #    member.save()
        with connection.cursor() as cursor:
            cursor.execute(query)
        print(f"Unprocessed Members: {members.count()}")

    