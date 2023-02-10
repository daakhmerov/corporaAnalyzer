def process_corpora_dataframes(input_gz_json_files_dir:str, df_output_dir:str='.\\df_output', df_logs_output_dir:str='.\\df_logs_output', start:int=0, end:int=-1):
    # Импорт сторонних модулей
    import os
    from tqdm import tqdm

    # Импорт локальных модулей
    from app import df_from_gzjson, log_it, printc_console_log

    # Программа
    ## Список, в котором содержатся пути к требуемым .pdf-файлам
    all_files = [f"{os.path.join(input_gz_json_files_dir, file)}" for file in os.listdir(input_gz_json_files_dir)][start:end]

    ## Переменные
    ### Список для хранения логов
    log_flow = []

    ## Обработка данных
    try:
        for file in tqdm(all_files):
            try:
                process_result = df_from_gzjson(file, df_output_dir)
                printc_console_log(process_result)
                log_flow.append(process_result)
            except:
                exception_log = {'status':'Danger', 'log_string':'-- Процесс прерван внутри цикла. Возможно, ошибка обработки данных--'}
                log_flow.append(exception_log)
        log_it(log_flow, df_logs_output_dir, 'df')
    except:
        exception_log = {'status':'Danger', 'log_string':'-- Процесс прерван вне цикла. Возможно, ошибка в программе--'}
        log_flow.append(exception_log)
        log_it(log_flow, df_logs_output_dir, 'df')