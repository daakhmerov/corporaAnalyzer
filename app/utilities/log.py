# Импорт сторонних библиотек
import compress_json as cj
from termcolor import colored


class LogString:
    status: str
    message: str

    def __init__(self, status: str, message: str):
        self.status = status
        self.message = message

    def pbash(self, color: str = 'white'):
        print(colored(f'\n{self.message}', color))

    def __repr__(self):
        return f"LogString(status='{self.status}', message='{self.message}')"

    def __str__(self):
        return f'{self.status.capitalize()}: {self.message}'

    def append_and_print(self, log_flow: list):
        self.pbash()
        self.append_to_flow(log_flow)

    def append_to_flow(self, log_flow: list):
        log_flow.append(self)


class Error_(LogString):
    def __init__(self, message: str, error: str | Exception | None):
        super().__init__(status='error', message=message)
        self.error = error

    def pbash(self):
        if self.error != None:
            print(colored(f'\n{self.message}\n↳{self.error}\n', 'red'))
        else:
            print(colored(f'\n{self.message}', 'red'))

    def append_and_print(self, log_flow: list):
        return super().append_and_print(log_flow)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__repr__()

    def append_to_flow(self, log_flow: list):
        return super().append_to_flow(log_flow)


class Success(LogString):
    def __init__(self, message: str):
        super().__init__(status='success', message=message)

    def append_and_print(self, log_flow: list):
        return super().append_and_print(log_flow)

    def pbash(self):
        super().pbash('green')

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__repr__()

    def append_to_flow(self, log_flow: list):
        return super().append_to_flow(log_flow)


class Warning(LogString):
    def __init__(self, message: str):
        super().__init__(status='warning', message=message)

    def pbash(self):
        return super().pbash('yellow')

    def append_and_print(self, log_flow: list):
        return super().append_and_print(log_flow)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__repr__()

    def append_to_flow(self, log_flow: list):
        return super().append_to_flow(log_flow)


class Log:
    def __init__(self, project_dir: str):
        self.flow = []
        self.project_dir = project_dir

    def to_json(self):
        # Импорт сторонних библиотек
        import os
        import json
        from datetime import datetime

        # Пути
        log_output_dir = os.path.join(self.project_dir, '.logs')

        # Переменные
        today = datetime.now()

        # Создание каталога для логов
        try:
            os.mkdir(log_output_dir)
        except:
            pass

        # Вывод данных
        data = [{'status': log.status, 'message': log.message if log.status !=
                 'error' else f'{log.message} → {log.error}'} for log in self.flow]
        cj.dump(
            data,
            os.path.join(log_output_dir,
                         f'log_{today.strftime("%b-%d-%Y %H-%M-%S")}.json.gz'),
            json_kwargs={'ensure_ascii': False}
        )
