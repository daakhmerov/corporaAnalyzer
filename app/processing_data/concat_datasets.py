def concat_datasets(data_dir):
    # Импорт сторонних модулей
    import pandas as pd
    import compress_json as cj
    import os

    # Обработка данных
    main_df = pd.concat([pd.read_json(cj.load(os.path.join(data_dir, file_path)), orient='table')
                        for file_path in os.listdir(data_dir)]).reset_index(drop=True)

    # Вывод данных
    return main_df
