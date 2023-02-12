def parse_filename(pdf_file_name:str):
    # Импорт необходимых библиотек
    import re
    import os

    # Обработка данных
    ## Только имя файла
    file_name = os.path.splitext(pdf_file_name)[0]
    ## Парсинг номера газеты
    number_pattern = r'№ \d+'
    
    full_number_parsed = re.findall(number_pattern, file_name)
    if len(full_number_parsed) > 0:
        number_parsed = re.findall(r'\d{1,3}', full_number_parsed[0])[0]
    else:
        number_parsed = None

    ## Парсинг названия
    name_pattern = r'[а-яА-Я]+'
    
    name_parsed = re.findall(name_pattern, file_name)
    if len(name_parsed) > 0:
        name_parsed = name_parsed[0]
    else:
        name_parsed = None

    ## Парсинг года
    year_pattern = r'\d{4}'
    
    year_parsed = re.findall(year_pattern, file_name)
    if len(year_parsed) > 0:
        year_parsed = year_parsed[0]
    else:
        year_parsed = None

    # Вывод данных
    result = {
        'newspaperName': name_parsed,
        'newspaperYear': year_parsed,
        'newspaperNumber': number_parsed
    }

    return result