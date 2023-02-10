def parse_issue_date(pdf_file_path:str):
    # Импорт сторонних модулей
    import os
    import PyPDF2
    import re
    from termcolor import colored

    # Ввод данных
    pdf_file = open(pdf_file_path, 'rb')

    # Обработка данных
    ## Создание объекта PdfFileReader
    reader = PyPDF2.PdfReader(pdf_file)

    ## Создание переменной "first page", "size_search_area", "search_area"  для текста первой страницы газеты, размеры зоны поиска строки и непосредственно зоны поиска строки, содержащей дату, соответственно
    first_page = reader.pages[0].extract_text()
    size_search_area = int(len(first_page)/10)
    search_area = first_page[0:size_search_area]

    ## Поиск даты выпуска газеты
    ### Патерн регулярного выражения для поиска даты выпуска газеты
    pattern = r'\d{1,2}\s{0,3}[а-яА-Я]+\s{0,3}\d{4}'
    try:
        full_date = [e.strip() for e in re.findall(pattern, search_area)[0].split(' ')]
        day, month, year = full_date[0], full_date[1], full_date[2]
        print(colored(f'-- Дата выпуска газеты "{os.path.split(pdf_file_path)[-1]}" успешно определена --', 'green'))
        return {'day':day, 'month':month, 'year': year}
    except:
        day, month, year = None, None, None
        print(colored(f'-- Дата выпуска газеты "{os.path.split(pdf_file_path)[-1]}" не определена --', 'red'))
        return {'day':day, 'month':month, 'year': year}