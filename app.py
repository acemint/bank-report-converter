import os
import pandas as pd
import logging
from banks import Banks, BCATransactionValidator
from extensions import FileExtensions

class Globals:
    bca_transation_validator: BCATransactionValidator
    logger: logging.Logger


def main():

    path_to_raw_resource = os.path.join(os.getcwd(), 'resource', 'raw')
    path_to_processed_resource = os.path.join(os.getcwd(), 'resource', 'processed')
    
    for category in os.listdir(path_to_raw_resource):

        path_to_raw_resource_with_category = os.path.join(path_to_raw_resource, category)
        path_to_processed_resource_with_category = os.path.join(path_to_processed_resource, category)
        if not os.path.exists(path_to_processed_resource_with_category):
            os.mkdir(path_to_processed_resource_with_category)

        if category == Banks.bca:
            
            for file_name in os.listdir(path_to_raw_resource_with_category):
                path_to_file = os.path.join(path_to_raw_resource_with_category, file_name)
                destination_csv = os.path.join(path_to_processed_resource_with_category, os.path.splitext(file_name)[0] + FileExtensions.csv)

                df = Globals.bca_transation_validator.process_data(path_to_file)

                Globals.logger.info("Processing file " + path_to_file)
                df.to_csv(destination_csv)


if __name__ == "__main__":
    Globals.bca_transation_validator = BCATransactionValidator()
    Globals.logger = logging.getLogger(__name__)
    main()

