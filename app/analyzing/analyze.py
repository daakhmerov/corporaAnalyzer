def analyze_project(project_dir: str, clean_data:bool=True):
    # Импорт сторонних библиотек
    import os

    # Импорт локальных библиотек
    from app import pipeline, LogString, log_to_json, log_to_html

    # Пути
    project_subdirs = [os.path.join(project_dir, subdir)
                       for subdir in os.listdir(project_dir)]

    # Log Flow
    log_flow = []

    # Обработка данных
    for subdir in project_subdirs:
        if os.path.split(subdir)[-1][0] != '.':
            log_flow.append(LogString('section', f'Корпус — {subdir}'))
            try:
                pipeline(subdir, log_flow, clean_data)
            except Exception as e:
                log_flow.append(
                    LogString('danger', f'Ошибка обработки корпуса\n⤷{e}\n'))

    # Создание логов
    log_to_json(log_flow, project_dir)
    log_to_html(log_flow, project_dir)
