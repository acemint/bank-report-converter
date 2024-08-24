import os
import pandas as pd
import logging
from banks import bank_data_type_validator_facade
from extensions import FileExtensions

class Globals:

    logger: logging.Logger


def main():

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

            Globals.logger.info("Processing file " + path_to_file)
            df.to_csv(destination_csv)


if __name__ == "__main__":
    Globals.logger = logging.getLogger(__name__)
    main()

