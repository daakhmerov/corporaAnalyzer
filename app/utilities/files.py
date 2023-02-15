import os


def check_extension(file_name: str, extension: str) -> bool:
    if os.path.splitext(file_name)[-1] == extension:
        return True
    else:
        return False


def get_file_paths(directory: str, extension: str | None = None, start: None | int = None, end: None | int = None) -> list | None:
    # Получение путей ко всем файлам внутри каталога
    if extension != None:
        all_files = [f"{os.path.join(directory, file)}" for file in os.listdir(
            directory) if file[0] != '.' and os.path.splitext(file)[-1] == extension]
    else:
        all_files = [f"{os.path.join(directory, file)}" for file in os.listdir(
            directory) if file[0] != '.']

    # Установка начального и/или конечного индексов среза списка с путями к датафреймам с токенами
    if start == None and end != None:
        return all_files[:end]
    elif start != None and end == None:
        return all_files[start:]
    elif start != None and end != None:
        return all_files[start:end]
    elif len(all_files) == 0:
        return None
    else:
        return all_files
