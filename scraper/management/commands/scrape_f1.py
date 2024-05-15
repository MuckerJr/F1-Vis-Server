from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import datetime
import json
from pymongo import MongoClient
from dateutil.parser import parse

class Command(BaseCommand):
    help = 'Scrapes the F1 website'

    def handle(self, *args, **options):
        client = MongoClient('mongodb+srv://visServer:Tk3cWqcWfMda040p@f1-visualised.pqqpwfw.mongodb.net/?retryWrites=true&w=majority&appName=F1-Visualised')
        db = client['F1-Visualised']
        collection = db['GPDates']

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
                if months_element:
                    months_text = months_element.text.strip()
                    # If there are multiple months, take the last one
                    months = months_text.split('-')[-1].strip()
                else:
                    months = None
                
                if end_date and months:
                    date_str = f'{end_date} {months} {current_year}'
                    date = parse(date_str)
                    date_str = date.strftime('%Y-%m-%d')

                race = {
                    'date': date_str,
                    'completed': False
                }

                races.append(race)
                try:
                    # Replace the document if it exists, insert it if it doesn't
                    result = collection.replace_one({'date': race['date']}, race, upsert=True)
                    print(f'Result: {result.raw_result}')  # Print the result of the operation
                except Exception as e:
                    print(f'Error: {e}')  # Print the error
                #collection.replace_one({'date' : race['date']}, race, upsert=True)

            return json.dumps(races)
        else:
            return 'Failed to fetch data from F1 website.'