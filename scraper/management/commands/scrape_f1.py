from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import datetime
import json

class Command(BaseCommand):
    help = 'Scrapes the F1 website'

    def handle(self, *args, **options):
        current_year = datetime.datetime.now().year
        response = requests.get(f'https://www.formula1.com/en/racing/{current_year}.html')
        print(f'https://www.formula1.com/en/racing/{current_year}.html')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            races = []
            # Find all race date elements
            race_elements = soup.find_all('div', class_="event-info")
            for element in race_elements:
                # Extract the end date
                end_date_element = element.find("span", class_="end-date")
                end_date = end_date_element.text.strip() if end_date_element else None

                # Extract the month(s)
                months_element = element.select_one("span.month-wrapper")
                print(f"Months Element: {months_element}")
                if months_element:
                    months_text = months_element.text.strip()
                    # If there are multiple months, take the last one
                    months = months_text.split('-')[-1].strip()
                else:
                    months = None

                races.append({
                    'end_date': end_date,
                    'month': months
                })
            return json.dumps(races)
        else:
            return 'Failed to fetch data from F1 website.'