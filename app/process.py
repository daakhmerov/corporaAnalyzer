def process_newspaper(pdf_file_path:str, output_path:str = '.'):
    # Импорт сторонних модулей
    import os
    import PyPDF2
    import compress_json as cj

    # Импорт локальных модулей
    from app import preprocess_text, word_tokenize_text, parse_filename, parse_issue_date

    # Ввод данных
    full_file_name = os.path.split(pdf_file_path)[-1]
    only_file_name = os.path.splitext(full_file_name)[0]
    pdf_file = open(pdf_file_path, 'rb')
    
    # Создание каталога для вывода 
    try:
        os.mkdir(output_path)
    except:
        pass

    # Обработка данных
    ## Создание объекта PdfFileReader
    reader = PyPDF2.PdfReader(pdf_file)

    ## Парсинг даты
    parsed_date = parse_issue_date(pdf_file_path)

    ## Создание переменной "pages", в которой хранится список предобработанных текстов, полученных с каждой из страниц газеты
    pages = [preprocess_text(page.extract_text()) for page in reader.pages]

    ## Обработка всех страниц газеты
    ### Создание словаря words, в котором будут храниться словари, содержащие информацию о токене, биграммах, странице газеты, названии газеты, номере газеты и года её издания
    words = []

    for index, page in enumerate(pages):
        tokens = word_tokenize_text(page)
        for token in tokens:
            token['fileName'] = full_file_name
            parsed_filename = parse_filename(only_file_name)

            token['page'] = str(index + 1)

            token['newspaperName'] = parsed_filename.get('newspaperName')
            token['newspaperYear'] = parsed_filename.get('newspaperYear')
            token['newspaperNumber'] = parsed_filename.get('newspaperNumber')
            
            token['newspaperMonth'] = parsed_date.get('month')
            token['newspaperDay'] = parsed_date.get('day')

            words.append(token)

    # Вывод данных
    cj.dump(words, f'{output_path}/{only_file_name}.json.gz', json_kwargs = {'ensure_ascii': False})
    return {'status':'Success', 'log_string':f'-- Файл "{os.path.split(pdf_file_path)[-1]}" успешно обработан --'}