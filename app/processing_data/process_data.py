def tokens_to_df(gz_json_file_path: str, output_dir: str):
    # Импорт сторонних модулей
    import os
    import pandas as pd
    import compress_json as cj

    # Импорт локальных модулей
    from app import LogString

    # Пути
    full_file_name = os.path.split(gz_json_file_path)[-1]
    only_file_name = os.path.splitext(os.path.splitext(full_file_name)[0])[0]

    # Ввод данных
    # Загрузка gz.json-файла с данными газеты
    newspaper_obj_list = cj.load(gz_json_file_path)

    # Создание каталога для вывода
    try:
        os.mkdir(output_dir)
    except:
        pass

    # Обработка данных
    # Столбцы
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

    # Перебор всех токенов и прочих соответствующих данных
    for index, value in enumerate(newspaper_obj_list):
        newspaper_obj = value

        # Чтение данных
        token = newspaper_obj.get('token')
        bigrams = ';'.join([' '.join(bigram)
                           for bigram in newspaper_obj.get('bigrams')])
        name = newspaper_obj.get('newspaperName')
        issue = newspaper_obj.get('newspaperNumber')
        page = newspaper_obj.get('page')
        day = newspaper_obj.get('newspaperDay')
        month = newspaper_obj.get('newspaperMonth')
        year = newspaper_obj.get('newspaperYear')
        filename = newspaper_obj.get('fileName')

        # Добавление данных в соотвествующий столбец словаря "data"
        data['token'].append(token)
        data['bigrams'].append(bigrams)
        data['name'].append(name)
        data['issue'].append(issue)
        data['page'].append(page)
        data['day'].append(day)
        data['month'].append(month)
        data['year'].append(year)
        data['filename'].append(filename)

    # Создание датафрейма
    df = pd.DataFrame(data)

    # Вывод xlsx.gz-файла датафрейма с данными газеты
    cj.dump(df.to_json(orient='table', index=False, force_ascii=False), os.path.join(
        output_dir, f'{only_file_name}.json.gz'), json_kwargs={'ensure_ascii': False})
    return LogString('success', f'Файл {full_file_name} успешно преобразован в pandas-датафрейм в формате JSON')
