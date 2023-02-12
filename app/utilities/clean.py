def delete_dir(dir: str, log_flow: list):
    # Импорт сторонних библиотек
    import shutil

    # Импорт локальных библиотек
    from app import LogString

    # Обработка данных
    try:
        shutil.rmtree(dir)
        log_flow.append(
            LogString('warning', f'Директория {dir} с промежуточными данными удалена'))
    except Exception as e:
        log_flow.append(LogString(
            'danger', f'Не удалось удалить директорию {dir} с промежуточными данными\n⤷{e}\n'))
