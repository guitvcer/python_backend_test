import schedule
import time
from django.core.management.base import BaseCommand
from airflow.services import load_currencies


class Command(BaseCommand):
    """Custom Management Command для обновления списка валют в БД"""

    help = "Обновляет список валют в БД"

    def handle(self, *args, **kwargs):
        self.job()

        schedule.every().day.at('12:00').do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self) -> None:
        load_currencies()
        self.stdout.write(self.style.SUCCESS("Currencies have been updated successfully!"))
