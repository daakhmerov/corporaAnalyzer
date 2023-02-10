def df_from_gzjson(gz_json_file_path:str, output_path:str = '.\\df_outputs', start_obj:int=0, end_obj:int=-1):
    # Импорт сторонних модулей
    import os
    import openpyxl
    import pandas as pd
    import compress_json as cj

    # Импорт локальных модулей
    from app import export_compress_df

    # Пути
    full_file_name = os.path.split(gz_json_file_path)[-1]
    only_file_name = os.path.splitext(os.path.splitext(full_file_name)[0])[0]

    # Ввод данных
    ## Загрузка gz.json-файла с данными газеты
    newspaper_obj_list= cj.load(gz_json_file_path)[start_obj:end_obj]

    # Создание каталога для вывода 
    try:
        os.mkdir(output_path)
    except:
        pass

    # Обработка данных
    ## Столбцы
    data = {
        'token': [],
        'bigrams': [],
        'name': [],
        'issue': [],
        'page': [],
        'day': [],
        'month': [],
        'year': [],
        'filename': []
    }

    ## Перебор всех токенов и прочих соответствующих данных
    for index, value in enumerate(newspaper_obj_list):
        newspaper_obj = value

        ### Чтение данных
        token = newspaper_obj.get('token')
        bigrams = ';'.join([' '.join(bigram) for bigram in newspaper_obj.get('bigrams')])
        name = newspaper_obj.get('newspaperName')
        issue = newspaper_obj.get('newspaperNumber')
        page = newspaper_obj.get('page')
        day = newspaper_obj.get('newspaperDay')
        month = newspaper_obj.get('newspaperMonth')
        year = newspaper_obj.get('newspaperYear')
        filename = newspaper_obj.get('fileName')

        ### Добавление данных в соотвествующий столбец словаря "data"
        data['token'].append(token)
        data['bigrams'].append(bigrams)
        data['name'].append(name)
        data['issue'].append(issue)
        data['page'].append(page)
        data['day'].append(day)
        data['month'].append(month)
        data['year'].append(year)
        data['filename'].append(filename)

    ### Создание датафрейма
    df = pd.DataFrame(data)

    # Вывод xlsx.gz-файла датафрейма с данными газеты
    export_compress_df(df, output=f'{output_path}\\{only_file_name}.xlsx.gz')
    return {'status':'Success', 'log_string':f'-- "Файл {full_file_name} успешно экспортирован в формате .xlsx" --'}