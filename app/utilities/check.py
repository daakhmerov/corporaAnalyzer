def check_pdf_file(pdf_file_path:str):
    # Импорт сторонних модулей 
    import PyPDF2
    import os

    # Импорт локальных модулей
    from app import LogString

    # Программа
    ## Проверка .pdf-файла
    try:
        try:
            reader = PyPDF2.PdfReader(pdf_file_path)

            for page in reader.pages:
                text = page.extract_text()  
                if len(text) == 0:
                    return LogString('danger', f'В файле "{os.path.split(pdf_file_path)[-1]}" не найден текстовый слой')
                else:
                    return LogString('warning', f'В файле "{os.path.split(pdf_file_path)[-1]}" найден текстовый слой')
        except FileNotFoundError:
            return LogString('danger', f'Файл "{os.path.split(pdf_file_path)[-1]}" не найден')
    except PyPDF2.errors.EmptyFileError:
        return LogString('danger', f'Файл "{os.path.split(pdf_file_path)[-1]}" пуст')
    except Exception as e:
        return LogString('danger', f'Файл "{os.path.split(pdf_file_path)[-1]}". Ошибка {e}')