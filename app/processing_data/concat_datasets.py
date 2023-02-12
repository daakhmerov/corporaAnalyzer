def concat_datasets(data_dir, log_flow:list):
    # Импорт сторонних модулей
    import pandas as pd
    import compress_json as cj
    import os

    # Импорт локальных модулей
    from app import LogString

    # Обработка данных
    dfs = []

    for file_path in (os.listdir(data_dir)):
        log_flow.append(LogString('warning', f'Обработка файла {file_path}'))

        if os.path.splitext(file_path)[-1] == '.gz':
            log_flow.append(LogString('warning', f'Чтение файла {file_path}...'))
            df = pd.read_json(cj.load(os.path.join(data_dir, file_path)), orient='table')
            log_flow.append(LogString('warning', f'Файл {file_path} загружен'))
            dfs.append(df)
            log_flow.append(LogString('warning', f'Файл {file_path} обработан'))

    main_df = pd.concat(dfs).reset_index(drop=True)
    log_flow.append(LogString('success', f'Датафрейм {file_path} создан'))

    # Вывод данных
    return main_df
