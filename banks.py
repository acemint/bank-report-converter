import pymupdf
import pandas as pd
import locale
from datetime import datetime
from extensions import FileExtensions
from calendar_utils import abbreviation

class BankDataType:
    bca_credit = 'bca_credit'
    bca_debit = 'bca_debit'


class BankDataTypeValidatorInterface:

    def process_data(self, path_to_file: str) -> pd.DataFrame:
        pass


class BCACreditCardTransactionValidator(BankDataTypeValidatorInterface):

    locale = "id_ID"

    def __init__(self):
        pass

    def process_data(self, path_to_file: str) -> pd.DataFrame:
        transaction_data = []

        if path_to_file.endswith(FileExtensions.pdf):
            pdf = pymupdf.open(path_to_file)

            for page in pdf:
                text_blocks = page.get_text("blocks")
                for text_block in text_blocks:
                    text_data = text_block[4].split('\n')
                    if self.is_valid_transaction(text_data):
                        transaction_data.append(text_data)
            return pd.DataFrame(transaction_data)
        else :
            raise Exception("Extension is not supported")

    def is_valid_transaction(self, text_component):
        date_format = "%d-%b"
        try:
            date_0 = self._convert_date_to_locale(text_component[0])
            date_1 = self._convert_date_to_locale(text_component[1])

            datetime.strptime(date_0, date_format)
            datetime.strptime(date_1, date_format)

            return True
            
        except ValueError:
            return False
        
    def _convert_date_to_locale(self, date: str):
        date_parts = date.split('-')

        if len(date_parts) == 2:
            date_parts[1] = abbreviation.convert_id_to_en(date_parts[1])
            return '-'.join(date_parts)
        return date


class BCADebitCardTransactionValidator(BankDataTypeValidatorInterface):

    locale = "id_ID"

    def __init__(self):
        pass

    def process_data(self, path_to_file: str) -> pd.DataFrame:
        transaction_data = []

        if path_to_file.endswith(FileExtensions.pdf):
            pdf = pymupdf.open(path_to_file)

            for page in pdf:
                text_blocks = page.get_text("blocks")
                for text_block in text_blocks:
                    text_data = text_block[4].split('\n')
                    if self.is_valid_transaction(text_data):
                        transaction_data.append(text_data)
            return pd.DataFrame(transaction_data)
        else :
            raise Exception("Extension is not supported")

    def is_valid_transaction(self, text_component):
        date_format = "%d/%m"
        try:
            date = text_component[0]

            datetime.strptime(date, date_format)
            return True
            
        except ValueError:
            return False


class BankDataTypeValidatorFacade:
    
    bca_credit_card_transation_validator: BCACreditCardTransactionValidator
    bca_debit_card_transation_validator: BCADebitCardTransactionValidator

    def __init__(self):
        self.bca_credit_card_transation_validator = BCACreditCardTransactionValidator()
        self.bca_debit_card_transaction_validator = BCADebitCardTransactionValidator()

    def process(self, category: str, path_to_file: str) -> pd.DataFrame:
        if category == BankDataType.bca_credit:
            return self.bca_credit_card_transation_validator.process_data(path_to_file)
        if category == BankDataType.bca_debit:
            return self.bca_debit_card_transaction_validator.process_data(path_to_file)

bank_data_type_validator_facade = BankDataTypeValidatorFacade()        