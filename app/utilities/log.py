# {'status':'Success', 'log_string':f'-- Файл "{os.path.split(pdf_file_path)[-1]}" успешно обработан --'}
class LogString:
    status: str
    message: str

    def __init__(self, status, message):
        self.status = status
        self.message = f'\n{message}, RAM: {self.return_ram_status()}'
        self.log = self.return_log()
        self.bash = self.print_to_bash()
        self.dict = self.to_dict()

    def return_log(self):
        # Импорт сторонних библиотек
        from termcolor import colored

        # Обработка данных
        if self.status == 'success':
            color = 'green'
        elif self.status == 'warning':
            color = 'yellow'
        elif self.status == 'danger':
            color = 'light_red'
        elif self.status == 'section':
            color = 'grey'
        else:
            color = 'red'

        return colored(self.message, color)

    def return_ram_status(self):
        import psutil
        import os

        # return the memory usage in percentage like top
        process = psutil.Process(os.getpid())
        mem = process.memory_percent()
        return round(mem, 2)

    def print_to_bash(self):
        print(self.return_log())

    def __repr__(self):
        return f'<LogString. Status: {self.status}, message: {self.message.strip()}>'

    def to_dict(self):
        return {'status': self.status, 'description': self.message.strip()}


def log_to_json(log_flow: list, project_dir: str):
    # Импорт сторонних библиотек
    import os
    import json
    from datetime import datetime

    # Пути
    log_output_dir = os.path.join(project_dir, '.logs')

    # Переменные
    today = datetime.now()

    # Создание каталога для логов
    try:
        os.mkdir(log_output_dir)
    except:
        pass

    # Вывод данных
    with open(os.path.join(log_output_dir, f'log_{today.strftime("%b-%d-%Y %H-%M-%S")}.json'), 'w+', encoding='utf-8') as log:
        data = [log.dict for log in log_flow]
        json.dump(data, log, ensure_ascii=False)


def log_to_html(log_flow: list, project_dir: str):
    # Импорт сторонних модулей
    import os
    from datetime import datetime

    # Пути
    log_output_dir = os.path.join(project_dir, '.logs')

    # Локальные переменные
    today = datetime.now()

    # Обработка данных
    # Создание списка log_html_fragments для хранения html-фрагментов с текстом лога
    log_html_fragments = []

    # Добавление html-элементов в список log_html_fragments
    for i, log in enumerate(log_flow):
        status = log.status
        string_text = log.message.strip()

        if status == 'success':
            html_code = f'<p style="color:#198754"><b>{i}</b>: {string_text}</p><hr><br>'
        elif status == 'warning':
            html_code = f'<p style="color:#ffc107"><b>{i}</b>: {string_text}</p><hr><br>'
        elif status == 'section':
            html_code = f'<h2 style="color:#181818">{string_text}</h2><br><br>'
        else:
            html_code = f'<p style="color:#dc3545"><b>{i}</b>: {string_text}</p><hr><br>'

        log_html_fragments.append(html_code)

    # Создание html-строки
    html_log_text = '\n'.join(log_html_fragments)

    # Вывод данных
    # Файл шаблона
    template = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <title>Log — {today.strftime("%b-%d-%Y %H-%M-%S")}</title>
    </head>
    <body>
        <div class="container">
            <div class = "row" style="margin-bottom:4rem; margin-top:4rem">
                <h1>Log — {today.strftime("%b-%d-%Y %H-%M-%S")}</h1>
            </div>
            <div class = "row">
                {html_log_text}
            </div>
        </div>
    </body>
    </html>
    '''
    # Создание каталога для логов
    try:
        os.mkdir(log_output_dir)
    except:
        pass

    # Вывод html-файла с логом
    with open(os.path.join(log_output_dir, f'log_{today.strftime("%b-%d-%Y %H-%M-%S")}.html'), 'w+', encoding='utf-8') as html:
        html.write(template)
