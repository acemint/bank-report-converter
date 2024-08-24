import os
import pandas as pd
import logging
from banks import BankDataType, BCACreditCardTransactionValidator, BCADebitCardTransactionValidator
from extensions import FileExtensions

class Globals:
    bca_credit_card_transation_validator: BCACreditCardTransactionValidator
    bca_debit_card_transaction_validator: BCADebitCardTransactionValidator
    logger: logging.Logger


def main():

    path_to_raw_resource = os.path.join(os.getcwd(), 'resource', 'raw')
    path_to_processed_resource = os.path.join(os.getcwd(), 'resource', 'processed')
    
    for category in os.listdir(path_to_raw_resource):

        path_to_raw_resource_with_category = os.path.join(path_to_raw_resource, category)
        path_to_processed_resource_with_category = os.path.join(path_to_processed_resource, category)
        if not os.path.exists(path_to_processed_resource_with_category):
            os.mkdir(path_to_processed_resource_with_category)

        if category == BankDataType.bca_credit:
            
            for file_name in os.listdir(path_to_raw_resource_with_category):
                path_to_file = os.path.join(path_to_raw_resource_with_category, file_name)
                destination_csv = os.path.join(path_to_processed_resource_with_category, os.path.splitext(file_name)[0] + FileExtensions.csv)

                df = Globals.bca_credit_card_transation_validator.process_data(path_to_file)

                Globals.logger.info("Processing file " + path_to_file)
                df.to_csv(destination_csv)
        
        if category == BankDataType.bca_debit:

            for file_name in os.listdir(path_to_raw_resource_with_category):
                path_to_file = os.path.join(path_to_raw_resource_with_category, file_name)
                destination_csv = os.path.join(path_to_processed_resource_with_category, os.path.splitext(file_name)[0] + FileExtensions.csv)

                df = Globals.bca_debit_card_transaction_validator.process_data(path_to_file)

                Globals.logger.info("Processing file " + path_to_file)
                df.to_csv(destination_csv)


if __name__ == "__main__":
    Globals.bca_credit_card_transation_validator = BCACreditCardTransactionValidator()
    Globals.bca_debit_card_transaction_validator = BCADebitCardTransactionValidator()
    Globals.logger = logging.getLogger(__name__)
    main()

