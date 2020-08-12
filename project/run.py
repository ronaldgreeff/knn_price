import os
import csv

class Main():

    def __init__(self, records='records.csv'):

        with open('records.csv', newline='') as csv_file:
            self.records = [row for row in csv.DictReader(csv_file)]

    def get_files(self):
        d = {}
        for vendor in os.listdir('data'):
            d[vendor] = [file for file in os.listdir('data/{}'.format(vendor))]

        self.files = d

if __name__ == '__main__':
    x = Main()
    x.get_files()
    
    for i in x.files:
        print(len(x.files[i]), i)
        for f in x.files[i]:
            print(' {}'.format(f))