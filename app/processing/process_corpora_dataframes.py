def process_corpora_dataframes(input_gz_json_files_dir: str, df_output_dir: str, log_flow: list, start=None, end=None):
    # Импорт сторонних модулей
    import os
    from tqdm import tqdm

    # Импорт локальных модулей
    from app import tokens_to_df, LogString

    # Программа
    # Список, в котором содержатся пути к требуемым .pdf-файлам
    all_files = [f"{os.path.join(input_gz_json_files_dir, file)}" for file in os.listdir(
        input_gz_json_files_dir)]
    if start == None and end != None:
        all_files = all_files[:end]
    elif start != None and end == None:
        all_files = all_files[start:]
    elif start != None and end != None:
        all_files = all_files[start:end]

    # Переменные
    # Обработка данных
    try:
        for file in tqdm(all_files):
            try:
                process_result = tokens_to_df(file, df_output_dir)
                log_flow.append(process_result)
            except Exception as e_1:
                log_flow.append(
                    LogString('danger', f'Ошибка в процессе обработки данных\n⤷{e_1}\n'))
    except Exception as e_2:
        log_flow.append(LogString('danger', f'Неизвестная ошибка\n⤷{e_2}\n'))
