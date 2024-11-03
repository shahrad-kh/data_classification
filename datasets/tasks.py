import csv
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Log


@shared_task
def export_daily_logs():
    """
    Export all Log entries from the previous day to a CSV file.
    """
    print("running export")
    # Define the date range for the previous day
    end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=1)

    # Filter logs from the previous day
    logs = Log.objects.filter(datetime__range=(start_date, end_date))
    print("got the logs")
    # Define file name with the previous day's date
    filename = f"logs_{start_date.date()}.csv"
    with open(filename, 'a+', newline='') as csvfile:
        log_writer = csv.writer(csvfile)
        log_writer.writerow(['User', 'Action', 'Text Instance', 'Updated_Field', 'Action_Details', 'DateTime'])

        for log in logs:
            log_writer.writerow([log.user, log.action, log.text_instance, log.updated_field, log.action_details, log.datetime])

    print(f"Exported logs to {filename}")
