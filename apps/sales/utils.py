from django.db import connection


def generate_gwp_report():
    with connection.cursor() as cursor:
        query = """
            SELECT distinct date_trunc('month', created), next_status, count(*)
            FROM public.policies_cyclestatusupdates where next_status = 'active'
            GROUP BY created, next_status
            ORDER BY date_trunc('month', created)
        """
        cursor.execute(query)
