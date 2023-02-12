def parse_issue_date(pdf_file_path: str, log_flow:list):
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
    pattern = r'\d{1,2}\s{0,3}[а-яА-Я]+\s{0,3}19\d{2}'

    # Определение всех вхождений дат
    all_occurences = [e.strip().split(' ')
                        for e in re.findall(pattern, search_area)]

    # Определение дня и года издания газеты на осн. подсчёта частотности
    try:
        day = Counter([entry[0]
                        for entry in all_occurences]).most_common(1)[0][0]
    except Exception as e:
        log_flow.append(LogString('danger', f'День выпуска газеты {os.path.split(pdf_file_path)[-1]} не определенf\n⤷{e}\n'))
        day = None

    try:
        year = Counter([entry[2]
                        for entry in all_occurences]).most_common(1)[0][0]
    except Exception as e_1:
        try:
            year = re.findall(r'\d{4}', os.path.splitext(os.path.split(pdf_file_path)[-1])[0])[0]
            log_flow.append(LogString('success', f'Год выпуска газеты {os.path.split(pdf_file_path)[-1]} не определен, но удалось произвести парсинг года выпуска в имени файла\n⤷{e_1}\n'))
        except Exception as e_2:
            log_flow.append(LogString('danger', f'Год выпуска газеты {os.path.split(pdf_file_path)[-1]} не определен\n⤷{e_2}\n'))
            year = None

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

        log_flow.append(LogString(
            'success', f'Дата выпуска газеты {os.path.split(pdf_file_path)[-1]} определена'))
    except Exception as e:
            log_flow.append(LogString('danger', f'Месяц выпуска газеты {os.path.split(pdf_file_path)[-1]} не определен\n⤷{e}\n'))
            month = None


    return {'day': day, 'month': month, 'year': year}