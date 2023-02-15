# Импорт сторонних библиотек
import os
import tarfile
from tqdm import tqdm
import shutil

# Импорт локальных библиотек
from ..utilities.log import Success, Error_, Warning


class Corpora:
    def __init__(self, path_to_pdfs: str, log_flow: list, output_data_directory: str | None = None, start: None | int = None, end: None | int = None):
        self.path_to_pdfs = path_to_pdfs
        self.output_data_directory = output_data_directory
        self.start = start
        self.log_flow = log_flow
        self.end = end

    def process_corpora(self):
        def process_documents(path_to_pdfs, path_to_datasets, log_flow):
            # Импорт локальных библиотек
            from app import Document, get_file_paths

            # Получение всех файлов в директории с .pdf-файлами
            all_pdf_files = get_file_paths(path_to_pdfs, '.pdf')

            # Перебор элементов в директории с .pdf-файлами, и анализ .pdf-файлов
            for path_to_pdf_file in tqdm(all_pdf_files):
                try:
                    Warning(f'Идёт обработка документа {path_to_pdf_file}...').append_and_print(
                        self.log_flow)

                    # Создание объекта Document
                    d = Document(path_to_pdf_file, path_to_datasets, log_flow)

                    # Проверка .pdf-документа
                    if d.check_status == 'success':
                        # Обработка текста .pdf-файла
                        d.process_document(output_format='parquet')
                    else:
                        continue
                except Exception as e:
                    Error_('При обработке {path_to_pdf_file} возникла ошибка', e).append_and_print(
                        self.log_flow)

        # Импорт локальных библиотек
        from app import get_file_paths

        # Путь к директории с датасетами
        temp_dir = os.path.join(self.path_to_pdfs, '.temp')

        # Анализ .pdf-файлов
        process_documents(self.path_to_pdfs, temp_dir, self.log_flow)

        # Получение всех файлов в директории с .parquet-файлами
        all_parquet_files = get_file_paths(temp_dir, '.gzip')

        # Вывод данных
        # Путь к директории .gzip-архива
        if self.output_data_directory == None:
            path_to_datasets_archive = os.path.join(self.path_to_pdfs, '.data')
        else:
            path_to_datasets_archive = self.output_data_directory

        # Создание директории для архива
        try:
            os.mkdir(path_to_datasets_archive)
        except FileExistsError:
            pass

        # Создание архива
        try:
            with tarfile.open(os.path.join(
                path_to_datasets_archive, f'{os.path.split(self.path_to_pdfs)[-1]}.tar.gz'
            ), 'w:gz') as tar:
                for parquet_file in all_parquet_files:
                    tar.add(parquet_file, recursive=False,
                            arcname=os.path.split(parquet_file)[-1])

            # Удаление директории с датасетами
            shutil.rmtree(temp_dir)
            Success(f'Обработка корпуса {self.path_to_pdfs} завершена!').append_and_print(
                self.log_flow)
        except Exception as e:
            Error_(f'К сожалению, корпус {self.path_to_pdfs} не удалось обработать', e).append_and_print(
                self.log_flow)
