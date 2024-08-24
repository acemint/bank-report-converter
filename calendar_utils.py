# Mapping Indonesian month abbreviations to English

class Abbreviation:
    id_to_en = {
        "JAN": "JAN", "FEB": "FEB", "MAR": "MAR", "APR": "APR",
        "MEI": "MAY", "JUN": "JUN", "JUL": "JUL", "AGU": "AUG",
        "SEP": "SEP", "OKT": "OCT", "NOV": "NOV", "DES": "DEC"
    }
    
    def convert_id_to_en(self, month: str):
        try:
            return self.id_to_en[month.upper()]
        except KeyError: 
            return month

abbreviation = Abbreviation()