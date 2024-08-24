import os
import pandas as pd
import logging
import argparse
from banks import bank_data_type_validator_facade
from extensions import FileExtensions


class Globals:

    logger: logging.Logger
    logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

def process_file():
    path_to_raw_resource = os.path.join(os.getcwd(), 'resource', 'raw')
    path_to_processed_resource = os.path.join(os.getcwd(), 'resource', 'processed')
    
    for category in os.listdir(path_to_raw_resource):
        
        path_to_raw_resource_with_category = os.path.join(path_to_raw_resource, category)
        # For some reason there is .DS_Store file in this which I can't delete
        try: 
            os.listdir(path_to_raw_resource_with_category)
        except NotADirectoryError:
            continue

        path_to_processed_resource_with_category = os.path.join(path_to_processed_resource, category)
        if not os.path.exists(path_to_processed_resource_with_category):
            os.mkdir(path_to_processed_resource_with_category)

        for file_name in os.listdir(path_to_raw_resource_with_category):
            path_to_file = os.path.join(path_to_raw_resource_with_category, file_name)
            destination_csv = os.path.join(path_to_processed_resource_with_category, os.path.splitext(file_name)[0] + FileExtensions.csv)

            df = bank_data_type_validator_facade.process(category=category, path_to_file=path_to_file)

            Globals.logger.info("Processing file successful: " + path_to_file)
            df.to_csv(destination_csv)

def combine():    
    path_to_processed_resource = os.path.join(os.getcwd(), 'resource', 'processed')

    list_df = []
    for category in os.listdir(path_to_processed_resource):
        # For some reason there is .DS_Store file in this which I can't delete
        try: 
            os.listdir(path_to_processed_resource)
        except NotADirectoryError:
            continue

        path_to_processed_resource_with_category = os.path.join(path_to_processed_resource, category)
        for file_name in os.listdir(path_to_processed_resource_with_category):
            path_to_file = os.path.join(path_to_processed_resource_with_category, file_name)
            list_df.append(pd.read_csv(path_to_file))

        destination_csv = os.path.join(path_to_processed_resource, 'combined', 'combined.csv')
        
    master_df = pd.concat(list_df, axis=0)
    master_df.to_csv(destination_csv)


def main():
    parser = argparse.ArgumentParser(description='Takes input for bank data type.')
    parser.add_argument('--combine', 
                        metavar='C', 
                        default=True,
                        type=bool,
                        action=argparse.BooleanOptionalAction,
                        help='Should the processed files be combined to one excel?')
    parser.set_defaults(combine=True)
    args: argparse.Namespace = parser.parse_args()
    
    process_file()
    if args.combine == True:
        combine()

    

if __name__ == "__main__":
    Globals.logger = logging.getLogger(__name__)
    main()

