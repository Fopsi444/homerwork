# main.py

import argparse
import ast
from FetchClass import SWAPIClient
from SWAPIDataManager import SWAPIDataManager
from processor.PeopleProcessor import PeopleProcessor
from processor.PlanetsProcessor import PlanetsProcessor

def main():

    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)


    manager.register_processor("people", PeopleProcessor())
    manager.register_processor("planets", PlanetsProcessor())


    parser = argparse.ArgumentParser(description='SWAPI Data Manager')
    parser.add_argument('--endpoint', '-e', help='Список сутностей через кому (наприклад, people,planets)', default='people,planets')
    parser.add_argument('--filters', '-f', help='JSON-рядок з фільтрами для кожної сутності', default='{"people": ["films", "species"], "planets": ["films", "residents"]}')
    parser.add_argument('--output', '-o', help='Ім\'я вихідного Excel-файлу', default='swapi_data.xlsx')

    args = parser.parse_args()
    endpoints = args.endpoint.split(',')


    try:
        filters = ast.literal_eval(args.filters)
        print("Parsed filters:", filters)


        for endpoint in endpoints:
            manager.fetch_entity(endpoint)
            if endpoint in filters:
                manager.apply_filter(endpoint, filters[endpoint])


        manager.save_to_excel(args.output)

    except ValueError as e:
        print("Невірний формат JSON:", e)

if __name__ == "__main__":
    main()
