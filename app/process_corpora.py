def process_corpora(input_files_dir:str, output_dir:str='.\\output', logs_output_dir:str='.\\logs_output'):
    # Импорт сторонних модулей
    import os
    from tqdm import tqdm

    # Импорт локальных модулей
    from app import check_pdf_file, process_newspaper, log_it, printc_console_log

    # Программа
    ## Список, в котором содержатся пути к требуемым .pdf-файлам
    all_files = [f"{os.path.join(input_files_dir, file)}" for file in os.listdir(input_files_dir)][0:6]

    ## Переменные
    ### Список для хранения логов
    log_flow = []

    ## Обработка данных
    try:
        for file in tqdm(all_files):
            checking_result = check_pdf_file(file)
            checking_status = checking_result.get('status')

            if checking_status == 'Warning':
                printc_console_log(checking_result)
                log_flow.append(checking_result)
                process_result = process_newspaper(file, output_dir)
                printc_console_log(process_result)
                log_flow.append(process_result)
            else:
                printc_console_log(checking_result)
                log_flow.append(checking_result)
        log_it(log_flow, logs_output_dir)
    except:
        exception_log = {'status':'Danger', 'log_string':'-- Процесс прерван --'}
        printc_console_log(exception_log)
        log_flow.append(exception_log)
        log_it(log_flow, logs_output_dir)