from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import datetime

class Command(BaseCommand):
    help = 'Scrapes the F1 website'

    def handle(self, *args, **options):
        current_year = datetime.datetime.now().year
        response = requests.get(f'https://www.formula1.com/en/racing/{current_year}.html')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            races = []
            # Find all race date elements
            race_elements = soup.find_all('div', class_="date-month f1-uppercase f1-wide--s")
            for element in race_elements:
                # Extract the end date
                end_date = element.find("span", class_="end-date").text.strip()
                # Extract the month(s)
                months_text = element.find("span", class_="month-wrapper").text.strip()
                # If there are multiple months, take the last one
                months= months_text.split('-')[-1].strip()
                races.append({
                    'end_date': end_date,
                    'month': months
                })
            return races
        else:
            return None