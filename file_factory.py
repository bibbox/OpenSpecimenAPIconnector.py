import xlrd
import csv
import pandas as pd

class File_factory():

    def __init__(self):
        pass

    def csv_from_excel(self, filename):

        wb = xlrd.open_workbook(filename)
        for item in wb.get_sheets():
            print(item)
            input()

    def pandas_from_excel(self, filename):
        wb = pd.read_excel(filename)

file_reader = File_factory()