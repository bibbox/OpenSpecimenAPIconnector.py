import xlrd
import csv
import pandas as pd

##TODO (general):

class File_factory():

    def __init__(self):
        pass

    def pandas_from_excel(self, excel):
        
        df = pd.read_excel(excel)
        return df
        
    def pandas_from_json(self, json):
        
        df = pd.read_json(json)
        return df
    
    def pandas_from_csv(self, csv_file):
        
        df = pd.read_csv(csv)
        return df