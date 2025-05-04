import pandas as pd

class ReadExcel:
    @staticmethod
    def read_excel(excel_file):
        excel_file = excel_file
        df = pd.read_excel(excel_file)
        return df