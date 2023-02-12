def pipeline(project_subdir:str, log_flow:list, clean_data:bool = True, start:int=None, end:int=None, to_project_dir:bool=False, project_dir:str=None):
    # Импорт сторонних библиотек
    import os
    import compress_json as cj

    # Импорт локальных библиотек
    from app import process_corpora, process_corpora_dataframes, concat_datasets, LogString, delete_dir

    # Пути
    data_output = os.path.join(project_subdir, 'data')
    if to_project_dir is True and project_dir != None:
        corpora_dataset_output = os.path.join(project_dir, 'project_datasets_output')
    else:
        corpora_dataset_output = os.path.join(project_subdir, 'corpora_dataset_output')
    corpora_tokens_output = os.path.join(project_subdir, 'tokens')

    # Обработка данных
    ## Обработка газет
    try:
        process_corpora(project_subdir, corpora_tokens_output, log_flow, start, end)
    except Exception as e:
        LogString('danger', 'Ошибка обработки корпуса газет\n⤷{e}\n')

    ## Обработка токенов и сопутствующих данных
    try:
        process_corpora_dataframes(corpora_tokens_output, data_output, log_flow, start, end)
    except Exception as e:
        log_flow.append(LogString('danger', 'Ошибка обработки токенов\n⤷{e}\n'))

    ## Создание общего датафрейма
    try:
        main_df = concat_datasets(data_output).to_json(orient='table', force_ascii=False)
        log_flow.append(LogString('success', f'Датасеты из директории {data_output} успешно объединены'))
    except Exception as e:
        log_flow.append(LogString('danger', 'Ошибка объединения датасетов\n⤷{e}\n'))

    ## Очистка директорий с промежуточными данными
    if clean_data is True:
        delete_dir(data_output, log_flow)
    
    # Вывод данных
    try:
        cj.dump(main_df, os.path.join(corpora_dataset_output, f'{os.path.split(project_subdir)[-1]}_corpora_dataset.json.gz'), json_kwargs = {'ensure_ascii': False})
        log_flow.append(LogString('success', f'Датасет "{os.path.split(project_subdir)[-1]}_corpora_dataset.json.gz" успешно создан'))
    except Exception as e:
        log_flow.append(LogString('danger', f'Ошибка вывода общего для корпуса датасета\n⤷{e}\n'))