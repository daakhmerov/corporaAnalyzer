# Импорт сторонних библиотек
import os

# Импорт локальных библиотек
from ..utilities.log import Log, Success, Error_, Warning


class Project:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.corpora_dirs = [os.path.join(self.project_dir, dir) for dir in os.listdir(
            self.project_dir) if dir[0] != '.']
        self.log = Log(self.project_dir)

    def analyze(self):
        # Импорт локальных библиотек
        from app import Corpora

        # Обработка данных
        log_flow = self.log.flow

        Warning(f'Обработка корпусов документов проекта {self.project_dir}').append_and_print(
            log_flow)
        for corpora_dir in self.corpora_dirs:
            Corpora(corpora_dir, log_flow, os.path.join(
                self.project_dir, '.data')).process_corpora()

        # Логи
        Success(f'Обработка корпусов проекта {self.project_dir} завершена!')
        self.log.to_json()
