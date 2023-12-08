import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget,QLineEdit,QStackedWidget
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

class ErrorAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setWindowTitle("Interface")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.analyze_button = QPushButton("Анализ данных")
        self.analyze_button.clicked.connect(self.analyze_data)
        self.layout.addWidget(self.analyze_button)
        self.deviation_button = QPushButton("Отклонения")
        self.deviation_button.clicked.connect(self.calculate_deviation)
        self.layout.addWidget(self.deviation_button)
        self.statistics_button = QPushButton("Статистика")
        self.statistics_button.clicked.connect(self.show_statistics)
        self.layout.addWidget(self.statistics_button)
        self.filter_button = QPushButton("Фильтр по отклонениям ")
        self.filter_button.clicked.connect(self.filter_by_deviation)
        self.layout.addWidget(self.filter_button)
        self.deviation_threshold_input = QLineEdit()
        self.deviation_threshold_input.setPlaceholderText("Введите число отклонения")
        self.layout.addWidget(self.deviation_threshold_input)
        self.deviation_threshold_input.returnPressed.connect(self.filter_by_deviation)
        self.start_date_input = QLineEdit()
        self.start_date_input.setPlaceholderText("Начальная дата формата 26.08.2022")
        self.layout.addWidget(self.start_date_input)
        self.end_date_input = QLineEdit()
        self.end_date_input.setPlaceholderText("Конечная дата формата формата 12.11.2022")
        self.layout.addWidget(self.end_date_input)
        self.filter_by_date_button = QPushButton("Фильтр по датам")
        self.filter_by_date_button.clicked.connect(self.filter_by_date_button_clicked)
        self.layout.addWidget(self.filter_by_date_button)
        self.group_month_button = QPushButton("Группировать по месяцам")
        self.group_month_button.clicked.connect(self.group_month_button_clicked)
        self.layout.addWidget(self.group_month_button)
        self.all_period_button = QPushButton("Группировать по годам")
        self.all_period_button.clicked.connect(self.all_period_button_clicked)
        self.layout.addWidget(self.all_period_button)
        self.date_month = QLineEdit()
        self.date_month.setPlaceholderText("Введите дату месяца формата 2022.02")
        self.layout.addWidget(self.date_month)
        self.filter_by_month_button = QPushButton("Фильтр по месяцу")
        self.filter_by_month_button.clicked.connect(self.filter_by_month_button_clicked)
        self.layout.addWidget(self.filter_by_month_button)
        self.stacked_widget = QStackedWidget()
        self.table_widget = QTableWidget()
        self.text_output = QTextEdit()
        self.stacked_widget.addWidget(self.table_widget)
        self.stacked_widget.addWidget(self.text_output)
        self.layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(self.layout)
    def analyze_data(self):
        self.stacked_widget.setCurrentIndex(0)
        file_name = 'dataset.csv'
        df = self.error(file_name)
        self.df_from_table = df
        self.table_widget.clear()
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
    def calculate_deviation(self):
        self.stacked_widget.setCurrentIndex(0)
        file_name = 'dataset.csv'
        df = self.error(file_name)
        df = self.deviation(df)
        self.table_widget.clear()
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
    def show_statistics(self):
        self.stacked_widget.setCurrentIndex(1)
        file_name = 'dataset.csv'
        df = self.error(file_name)
        df = self.deviation(df)
        stat_info = df[['value', 'median_deviation', 'mean_deviation', 'calculated_column']].describe()
        self.text_output.clear()
        self.text_output.append(stat_info.to_string())
        plt.figure(figsize=(10, 6))
        df[['value', 'median_deviation', 'mean_deviation', 'calculated_column']].boxplot()
        plt.title("Boxplot для курса и отклонений")
        plt.show()
    def error(self, dataframe):
        df = pd.read_csv(dataframe, sep=';')
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['value'] = df['value'].replace('невалидное значение', np.nan)
        df = df[df['value'].notna()]
        return df
    def deviation(self, dataframe):
        dataframe['median_deviation'] = dataframe['value'].median() - dataframe['value']
        dataframe['mean_deviation'] = dataframe['value'].mean() - dataframe['value']
        dataframe['calculated_column'] = dataframe['median_deviation'] + dataframe['mean_deviation']
        return dataframe
    def filter_by_deviation(self,deviation_threshold):
        self.stacked_widget.setCurrentIndex(0)
        deviation_threshold = int(self.deviation_threshold_input.text())  
        file_name = 'dataset.csv'
        df = self.error(file_name)
        df = self.deviation(df)
        filtered_df = df[df['mean_deviation'] >= deviation_threshold]
        self.table_widget.clear()
        self.table_widget.setRowCount(filtered_df.shape[0])
        self.table_widget.setColumnCount(filtered_df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(filtered_df.columns)
        for row in range(filtered_df.shape[0]):
            for col in range(filtered_df.shape[1]):
                item = QTableWidgetItem(str(filtered_df.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
    def filter_by_date_button_clicked(self):
        start_date = self.start_date_input.text()
        end_date = self.end_date_input.text()
        self.filter_by_date(start_date, end_date)
    def filter_by_date(self,start_date, end_date):
        self.stacked_widget.setCurrentIndex(0)
        file_name = 'dataset.csv'
        df = self.error(file_name)
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
        start_date = pd.to_datetime(start_date, format='%d.%m.%Y')
        end_date = pd.to_datetime(end_date, format='%d.%m.%Y')
        filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        self.table_widget.clear()
        self.table_widget.setRowCount(filtered_df.shape[0])
        self.table_widget.setColumnCount(filtered_df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(filtered_df.columns)
        for row in range(filtered_df.shape[0]):
            for col in range(filtered_df.shape[1]):
                item = QTableWidgetItem(str(filtered_df.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
    def group_month_button_clicked(self):
        self.group_month()
    def group_month(self):
        self.stacked_widget.setCurrentIndex(0)
        file_name = 'dataset.csv'
        dataframe = self.error(file_name)
        dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d.%m.%Y', errors='coerce')
        monthly_avg = dataframe.groupby(dataframe['date'].dt.to_period("M")).agg({'value': 'mean'}).reset_index()
        self.table_widget.clear()
        self.table_widget.setRowCount(monthly_avg.shape[0])
        self.table_widget.setColumnCount(monthly_avg.shape[1])
        self.table_widget.setHorizontalHeaderLabels(monthly_avg.columns)
        for row in range(monthly_avg.shape[0]):
            for col in range(monthly_avg.shape[1]):
                item = QTableWidgetItem(str(monthly_avg.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_avg['date'].astype(str), monthly_avg['value'], marker='o')
        plt.title("Среднее значение курса по месяцам")
        plt.xlabel("Месяц")
        plt.ylabel("Среднее значение курса")
        plt.xticks(rotation=45)  
        plt.tight_layout()
        plt.show()
    def all_period_button_clicked(self):
        self.all_period()
    def all_period(self):
        self.stacked_widget.setCurrentIndex(0)
        file_name = 'dataset.csv'
        dataframe = self.error(file_name)
        df = dataframe.sort_values(by='date')
        sns.set(style="whitegrid")
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='date', y='value', data=df, marker='o', label='Курс')
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.title('График изменения курса за весь период')
        plt.xlabel('Год')
        plt.ylabel('Курс')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    def plot_currency_stats_for_month(self, target_month_year):
        self.stacked_widget.setCurrentIndex(0)
        file_name = 'dataset.csv'
        dataframe = self.error(file_name)
        dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d.%m.%Y', errors='coerce')
        target_month = pd.to_datetime(target_month_year, format='%Y.%m', errors='coerce')
        filtered_data = dataframe[(dataframe['date'].dt.month == target_month.month) & (dataframe['date'].dt.year == target_month.year)]
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='date', y='value', data=filtered_data, marker='o', label='Курс')
        plt.axhline(y=filtered_data['value'].mean(), color='red', linestyle='dashed', label='Среднее значение')
        plt.axhline(y=filtered_data['value'].median(), color='green', linestyle='dashed', label='Медиана')
        plt.title(f'График изменения курса за {target_month_year}')
        plt.xlabel('Дата')
        plt.ylabel('Курс')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    def filter_by_month_button_clicked(self):
        date_month = self.date_month.text()
        self.plot_currency_stats_for_month(date_month)
def main():
    app = QApplication(sys.argv)
    window = ErrorAnalyzerApp()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
