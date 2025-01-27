import argparse
import ast
import logging
from FetchClass import SWAPIClient
from SWAPIDataManager import SWAPIDataManager



def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(__name__)



def parse_arguments():
    parser = argparse.ArgumentParser(description='SWAPI Data Fetch and Process')
    parser.add_argument('--endpoint', '-e', help='Comma separated list of endpoints', default='people,planets')
    parser.add_argument('--filters', '-f', help='JSON format string of filters',
                        default='{"people": ["films", "species"], "planets": ["films", "residents"]}')
    parser.add_argument('--output', '-o', help='Output Excel file name', default='swapi_data.xlsx')

    args = parser.parse_args()

    try:

        filters = ast.literal_eval(args.filters)
    except (ValueError, SyntaxError) as e:
        logger.error("Invalid filters format: %s", e)
        filters = {}

    return args.endpoint.split(','), filters, args.output


def main():
    # Setup
    global logger
    logger = setup_logging()

    endpoints, filters, output_file = parse_arguments()


    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)


    for endpoint in endpoints:
        manager.fetch_entity(endpoint)
        if endpoint in filters:
            manager.apply_filter(endpoint, filters.get(endpoint, []))
    manager.save_to_excel(output_file)


if __name__ == "__main__":
    main()