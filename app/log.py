def printc_console_log(log_object):
    # Импорт сторонних библиотек
    from termcolor import colored

    # Переменные
    status = log_object.get('status')
    log_string = log_object.get('log_string')

    # Обработка данных
    if status == 'Success':
        color = 'green'
    elif status == 'Warning':
        color = 'yellow'
    elif status == 'Danger':
        color = 'red'
    else:
        color = 'light_red'
    
    print(colored(log_string, color))
    

def log_it(log_flow:list, output_path:str = './logs'):
    # Импорт сторонних модулей
    import os
    from datetime import datetime

    # Локальные переменные
    today = datetime.now()

    # Обработка данных
    ## Создание списка log_html_fragments для хранения html-фрагментов с текстом лога
    log_html_fragments = []

    ## Добавление html-элементов в список log_html_fragments
    for i, log_object in enumerate(log_flow):
        status = log_object.get('status')
        string_text = log_object.get('log_string')

        if status == 'Success':
            html_code = f'<p style="color:#198754"><b>{i}</b>: {string_text}</p><hr><br>'
        elif status == 'Warning':
            html_code = f'<p style="color:#ffc107"><b>{i}</b>: {string_text}</p><hr><br>'
        else:
            html_code = f'<p style="color:#dc3545"><b>{i}</b>: {string_text}</p><hr><br>'

        log_html_fragments.append(html_code)

    ## Создание html-строки
    html_log_text = '\n'.join(log_html_fragments)

    # Вывод данных
    ## Файл шаблона
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
    ## Создание каталога для логов
    try:
        os.mkdir(output_path)
    except:
        pass
    
    ## Вывод html-файла с логом
    with open(f'{output_path}/log_{today.strftime("%b-%d-%Y %H-%M-%S")}.html', 'w+', encoding='utf-8') as html:
        html.write(template)


