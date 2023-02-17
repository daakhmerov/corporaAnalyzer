# Импорт сторонних библиотек
import os
import PyPDF2
import pandas as pd
import numpy as np

# Импорт локальных библиотек
from ..process.parsemeta import parse_filename, parse_issue_date
from ..process.preprocess import preprocess_text
from ..process.tokenize import word_tokenize_text
from ..utilities.log import Success, Error_, Warning


class Document:
    def __init__(self, path_to_pdf: str, output_path: str, log_flow: list):
        self.path_to_pdf = path_to_pdf  # Путь к .pdf-файлу
        # Путь к директории, в которой хранятся токены и сопутствующая информация
        self.output_path = output_path
        self.log_flow = log_flow
        self.file_name = os.path.split(self.path_to_pdf)[-1]
        self.check_status = self.check_document()

        # Атрибуты только для газет. Далее будут вынесены в отдельный класс
        self.day, self.month, self.year = parse_issue_date(
            self.path_to_pdf, self.log_flow).values()
        self.name, self.fn_year, self.issue = parse_filename(
            self.file_name).values()

    def check_document(self):
        # Чтение .pdf-файла
        reader = PyPDF2.PdfReader(self.path_to_pdf)
        text = ''.join([page.extract_text() for page in reader.pages])

        if len(text) == 0:
            m = Warning(
                f'В документе {self.path_to_pdf} отсутствует текстовый слой')
            m.append_and_print(self.log_flow)
            return m.status
        else:
            m = Success(
                f'В документе {self.path_to_pdf} присутствует текстовый слой')
            m.append_and_print(self.log_flow)
            return m.status

    def process_document(self, output_format: str = 'parquet'):
        # Функции
        def generate_index(postfix: str | None = None):
            # Импорт сторонних библиотек
            import string
            import random

            chars = list(string.ascii_lowercase) + \
                [str(x) for x in range(6)]  # Список символов

            index = []
            for _ in range(6):
                index.append(random.choice(chars))
            if postfix != None:
                return ''.join(index) + '_' + str(postfix)
            else:
                return ''.join(index)

        try:
            # Чтение .pdf-файла
            pdf_file = open(self.path_to_pdf, 'rb')
            reader = PyPDF2.PdfReader(pdf_file)

            # Обработка .pdf-файла
            # Извлечение текстов со страниц и предобработка текстов
            pages = [preprocess_text(page.extract_text())
                     for page in reader.pages]

            # Токенизация и создание датафрейма
            Warning(f'Идёт токенизация текстового слоя документа {self.path_to_pdf}...').append_and_print(
                self.log_flow)
            list_tokens_dicts = []

            for index, page in enumerate(pages):
                tokens = word_tokenize_text(page)  # Токенизация страницы
                for token in tokens:
                    # Для всех документов
                    token['id'] = generate_index(self.year)
                    token['filename'] = self.file_name
                    token['page'] = str(index + 1)
                    token['bigrams'] = str(token.get('bigrams'))

                    # Только для газет
                    token['newspaper_name'], token['newspaper_issue'] = self.name, self.issue
                    token['newspaper_day'], token['newspaper_month'] = self.day, self.month.lower(
                    ) if type(self.month) == str else self.month
                    token['newspaper_year'] = self.fn_year if self.year == None else self.year

                    list_tokens_dicts.append(token)

            # Вывод данных
            # Создание директории для вывода файла с токенами
            try:
                os.mkdir(self.output_path)
            except FileExistsError:
                pass

            # Типы данных в датафрейме, в котором будут содержаться токены и прочая информация
            types = {
                'id': 'str',
                'token': 'str',
                'bigrams': 'str',
                'filename': 'category',
                'page': np.int8,
                'newspaper_name': 'category',
                'newspaper_issue': np.int8,
                'newspaper_day': np.int8,
                'newspaper_month': 'category',
                'newspaper_year': np.int16
            }

            # Создание датафрейма
            df = pd.DataFrame.from_dict(
                list_tokens_dicts).astype(types).set_index('id')
            output_file_path = os.path.join(
                self.output_path, f'{os.path.splitext(self.file_name)[0]}.{output_format}')

            if output_format == 'feather':
                df.to_feather(f"{output_file_path}.feather",
                              compression='zstd')
            else:
                df.to_parquet(f"{output_file_path}.gzip", compression='gzip')
            Success(f'Обработка документа {self.path_to_pdf} успешно завершена!').append_and_print(
                self.log_flow)
        except Exception as e:
            Error_(f'При обработке документа {self.path_to_pdf} произошла ошибка', e).append_and_print(
                self.log_flow)
