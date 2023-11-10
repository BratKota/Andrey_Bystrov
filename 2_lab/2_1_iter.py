#итератор
import os
import pandas as pd
from datetime import datetime, timedelta

class DateIterator:
    def __init__(self, input_csv_file):
        self.df = pd.read_csv(input_csv_file, delimiter=';', parse_dates=['Date'], dayfirst=True)
        self.dates = sorted(self.df['Date'].unique())
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.dates):
            target_date = self.dates[self.index]
            data_for_date = self.df[self.df['Date'] == target_date]

            self.index += 1

            if not data_for_date.empty:
                return self.index, target_date, data_for_date
        raise StopIteration

def create_dataset_from_files(files):
    return pd.concat([pd.read_csv(file, delimiter=';', parse_dates=['Date'], dayfirst=True) for file in files])

def save_new_dataset(file_to_save, file_to_read, index_custom=False):
    dataset = create_dataset_from_files(file_to_read)
    dataset.to_csv(file_to_save, index=index_custom)


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    input_csv_file = os.path.join(current_directory, "dataset.csv")
    iterator = DateIterator(input_csv_file)
    for iteration, date, data in iterator:
        formatted_date = date.strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD
        print(f"Итерация:{iteration} Дата: {formatted_date}, Данные: {formatted_date} : {data['Value'].values[0]}")

if __name__ == "__main__":
    main()
