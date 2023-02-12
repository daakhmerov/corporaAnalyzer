def process_corpora(input_files_dir: str, output_dir: str, log_flow: list, start=None, end=None):
    # Импорт сторонних модулей
    import os
    from tqdm import tqdm

    # Импорт локальных модулей
    from app import check_pdf_file, process_newspaper, LogString, made_checkpoint

    # Программа
    # Список, в котором содержатся пути к требуемым .pdf-файлам
    all_files = [f"{os.path.join(input_files_dir, file)}" for file in os.listdir(
        input_files_dir)]
    if start == None and end != None:
        all_files = all_files[:end]
    elif start != None and end == None:
        all_files = all_files[start:]
    elif start != None and end != None:
        all_files = all_files[start:end]

    # Обработка данных
    try:
        for file in tqdm(all_files):
            if os.path.splitext(file)[-1] == '.pdf':
                # Проверка .pdf-файла
                checking_result = check_pdf_file(file)
                checking_status = checking_result.status

                # Лог
                log_flow.append(checking_result)

                if checking_status == 'warning':
                    process_result = process_newspaper(
                        file, log_flow, output_dir)
                    log_flow.append(process_result)
                    made_checkpoint(output_dir)
            else:
                continue

    except ModuleNotFoundError as m_e:
        log_flow.append(LogString(
            'danger', f'Процесс прерван, т.к. не установлен следующий модуль\n⤷{m_e}\n'))
    except Exception as e:
        log_flow.append(
            LogString('danger', f'Процесс прерван из-за следующей ошибки\n⤷{e}\n'))
