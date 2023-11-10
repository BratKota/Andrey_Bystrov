import os
import sys
import pandas as pd
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, QLineEdit


class CSVViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.init_ui()

    def init_ui(self):
        # Создаем виджеты
        self.label = QLabel('Данные из CSV файла:')
        self.table_widget = QTableWidget()

        # Создаем кнопку для выбора нового файла
        self.choose_file_button = QPushButton('Выбрать CSV файл')
        self.choose_file_button.clicked.connect(self.choose_file)

        # Создаем кнопки для выполнения разбивки на X и Y, и выполнения второго файла
        self.execute_x_button = QPushButton('X')
        self.execute_x_button.clicked.connect(lambda: self.execute_first_file('X'))

        self.execute_y_button = QPushButton('Y')
        self.execute_y_button.clicked.connect(lambda: self.execute_first_file('Y'))
       
        self.execute_first_file_button = QPushButton('1')
        self.execute_first_file_button.clicked.connect(lambda: self.execute_first_file('1'))

        # Создаем кнопки для второго 
        self.execute_second_file_button = QPushButton('2')
        self.execute_second_file_button.clicked.connect(lambda: self.execute_second_file('2'))

        self.execute_z_button = QPushButton('Посмотреть')
        self.execute_z_button.clicked.connect(lambda: self.execute_second_file('Посмотреть'))

        # Создаем кнопки для третьего  
      
        self.execute_third_file_button = QPushButton('3')
        self.execute_third_file_button.clicked.connect(lambda: self.execute_second_file('3'))

       # 4 задание
        self.text_field = QLineEdit(self)
        self.execute_four_file_button = QPushButton('Получить данные')
        self.execute_four_file_button.clicked.connect(lambda: self.execute_second_file('Получить данные'))

        # Создаем главный макет
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.execute_first_file_button)
        button_layout.addWidget(self.execute_x_button)
        button_layout.addWidget(self.execute_y_button)

        third_layout = QHBoxLayout()
        third_layout.addWidget(self.execute_third_file_button)

        extra_button_layout = QHBoxLayout()

        extra_button_layout.addWidget(self.execute_second_file_button)
        extra_button_layout.addWidget(self.execute_z_button)

        

        four_layout = QHBoxLayout()
        four_layout.addWidget(self.text_field)
        four_layout.addWidget(self.execute_four_file_button)


      

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.table_widget)
        main_layout.addWidget(self.choose_file_button)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(extra_button_layout)
        main_layout.addLayout(third_layout)
        main_layout.addLayout(four_layout)
        

        # Назначаем макет виджету
        self.setLayout(main_layout)

        # Устанавливаем параметры окна
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('CSV Viewer')

    def choose_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_path, _ = file_dialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            self.file_path = file_path
            self.load_csv_data()

    def load_csv_data(self):
        if self.file_path:
            # Чтение данных из CSV-файла
            data = pd.read_csv(self.file_path, sep=';')

            # Устанавливаем количество строк и столбцов в таблице
            self.table_widget.setRowCount(data.shape[0])
            self.table_widget.setColumnCount(data.shape[1])

            # Заполняем таблицу данными
            self.table_widget.setHorizontalHeaderLabels(data.columns)
            for row in range(data.shape[0]):
                for col in range(data.shape[1]):
                    item = QTableWidgetItem(str(data.iloc[row, col]))
                    self.table_widget.setItem(row, col, item)

            # Обновляем интерфейс
            self.label.setText(f'Данные из CSV файла: {self.file_path}')
    #Методы нажатий для 1 кнопки 
    def execute_first_file(self, button_text):
        if button_text == '1':
            # Получаем путь к текущему каталогу
            current_directory = os.path.dirname(os.path.abspath(__file__))
            # Формируем путь к нашему скрипту
            script_path = os.path.join(current_directory, '1.py')
            # Выполняем скрипт с помощью subprocess
            subprocess.run(['python', script_path])
            self.label.setText(f'Скрипт выполнен')
        if button_text in ['X', 'Y']:
            folder_name = 'X_Y'
            folder_path = os.path.join(os.path.dirname(self.file_path), folder_name)

            # Формируем путь к файлу в папке 'папка'
            first_file_path = os.path.join(folder_path, f'{button_text}.csv')

            # Проверяем, существует ли файл
            if os.path.exists(first_file_path):
                # Чтение данных из второго CSV-файла
                first_data = pd.read_csv(first_file_path, sep=';')

                # Устанавливаем количество строк и столбцов в таблице
                self.table_widget.setRowCount(first_data.shape[0])
                self.table_widget.setColumnCount(first_data.shape[1])

                # Заполняем таблицу данными
                self.table_widget.setHorizontalHeaderLabels(first_data.columns)
                for row in range(first_data.shape[0]):
                    for col in range(first_data.shape[1]):
                        item = QTableWidgetItem(str(first_data.iloc[row, col]))
                        self.table_widget.setItem(row, col, item)

                # Обновляем интерфейс
                self.label.setText(f'Файл: {first_file_path}')
            else:
                self.label.setText(f'Файл {button_text}.csv не найден в папке {folder_name}')

            
    #Методы для 2 кнопки 
    def execute_second_file(self, button_text): 
         if button_text == '2':
            current_directory = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_directory, '2.py')
            subprocess.run(['python', script_path])
            self.label.setText(f'Скрипт выполнен')
         if button_text == '3':
            current_directory = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(current_directory, '3.py')
            subprocess.run(['python', script_path])
            self.label.setText(f'Скрипт выполнен')
         if button_text == 'Получить данные':
            target_date = datetime.strptime(self.text_field.text(), "%d.%m.%Y")
            if target_date:
                current_directory = os.path.dirname(os.path.abspath(__file__))
                script_path = os.path.join(current_directory, '4.py')
                subprocess.run(['python', script_path, target_date.strftime("%Y-%m-%d")])
                result = subprocess.run(['python', script_path, target_date.strftime("%Y-%m-%d")], capture_output=True, text=True)
                if result.returncode == 0:
                    number_from_script = result.stdout.strip()
                    print(number_from_script)
                    self.label.setText(f'Число из скрипта: {number_from_script}')
                else:
                    print(f"Ошибка выполнения скрипта: {result.stderr}")
                    self.label.setText('Ошибка выполнения скрипта')


                
            else:
                self.label.setText('Введите дату в поле')
         if button_text == 'Посмотреть':
             self.choose_file()
            


def main():
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
