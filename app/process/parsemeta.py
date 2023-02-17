# Импорт локальных библиотек
from ..utilities.log import Warning, Success, Error_, LogString


def parse_filename(pdf_file_name: str):
    # Импорт необходимых библиотек
    import re
    import os

    # Обработка данных
    # Только имя файла
    file_name = os.path.splitext(pdf_file_name)[0]
    # Парсинг номера газеты
    number_pattern = r'№ \d+'

    full_number_parsed = re.findall(number_pattern, file_name)
    if len(full_number_parsed) > 0:
        number_parsed = re.findall(r'\d{1,3}', full_number_parsed[0])[0]
    else:
        number_parsed = None

    # Парсинг названия
    name_pattern = r'[а-яА-Я]+'

    name_parsed = re.findall(name_pattern, file_name)
    if len(name_parsed) > 0:
        name_parsed = name_parsed[0]
    else:
        name_parsed = None

    # Парсинг года
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


def parse_issue_date(pdf_file_path: str, log_flow: list):
    # Импорт сторонних модулей
    import os
    import PyPDF2
    from collections import Counter
    from Levenshtein import ratio
    import re

    # Импорт локальных модулей
    from app import LogString

    # Ввод данных
    pdf_file = open(pdf_file_path, 'rb')

    # Обработка данных
    # Создание объекта PdfFileReader
    reader = PyPDF2.PdfReader(pdf_file)

    # Создание зоны поиска в верхнем колонтитуле на всех страницах документа
    search_areas = []

    for page in reader.pages:
        analyzed_page = page.extract_text()

        size_search_area = int(len(analyzed_page)/10)
        search_areas.append(analyzed_page[0:size_search_area])

    # Фрагмент текста документа, в котором будет происходить поиск даты
    search_area = ' '.join(search_areas).replace('\n', ' ')

    # Поиск даты выпуска газеты
    # Патерн регулярного выражения для поиска даты выпуска газеты
    pattern = r'\d{1,2}\s{0,3}[а-яА-Я]+\s{0,3}19[5-9]{1}[0-9]{1}'

    # Определение всех вхождений дат
    def parse_occurence(occurence:str):
        # Парсинг числа в строке
        day = re.search(r'\d{1,2}', occurence).group(0)
        if int(day) > 31:
            day = 0
        else:
            day = int(day)

        month = re.search(r'[а-яА-Я]+', occurence).group(0)
        if len(month) == 0:
            month = 'не определен'

        year = re.search(r'19[5-9]{1}[0-9]{1}', occurence).group(0)
        if len(year) == 0:
            year = 1001
        else:
            year = int(year)
        return [day, month, year]
                
        
    all_occurences = [parse_occurence(e) for e in re.findall(
        pattern, search_area)]

    print(all_occurences)

    # Определение дня издания газеты на осн. подсчёта частотности
    try:
        day = Counter([entry[0]
                       for entry in all_occurences]).most_common(1)[0][0]

    except Exception as e:
        Error_(f'В газете {pdf_file_path} не удалось определить день выпуска',
               e).append_and_print(log_flow)
        day = 0

    # Определение года издания газеты на осн. подсчёта частотности
    try:
        year = Counter([entry[2]
                        for entry in all_occurences]).most_common(1)[0][0]
    except:
        try:
            year = re.findall(r'\d{4}', os.path.splitext(
                os.path.split(pdf_file_path)[-1])[0])[0]
        except Exception as e_inner:
            Error_(f'В газете {pdf_file_path} не удалось определить год выпуска',
                   e_inner).append_and_print(log_flow)
            year = 1001

    # Определение месяца издания газеты на осн. подсчёта частотности и нормализованного сходства перестановки
    try:
        def check_month_similarity(found_month: str):
            months = [
                'января',
                'февраля',
                'марта',
                'апреля',
                'мая',
                'июня',
                'июля',
                'августа',
                'сентября',
                'октября',
                'ноября',
                'декабря'
            ]

            for month in months:
                if ratio(month, found_month) > 0.5:
                    return month
                else:
                    return found_month

        month = Counter([check_month_similarity(entry[1])
                        for entry in all_occurences]).most_common(1)[0][0]
    except Exception as e:
        Error_(f'В газете {pdf_file_path} не удалось определить месяц выпуска',
               e).append_and_print(log_flow)
        month = 'не определен'

    if day != 0 and month != 'не определен' and year != 1001:
        Success(f'Дата выпуска газеты {pdf_file_path} полностью определена!').append_and_print(
            log_flow)
    elif day == 0 or month == 'не определен' or year == 1001:
        Warning(f'Дата выпуска газеты {pdf_file_path} определена частично').append_and_print(
            log_flow)
    else:
        Error_(f'Дата выпуска газеты {pdf_file_path} не определена', None).append_and_print(
            log_flow)

    return {'day': day, 'month': month, 'year': year}
