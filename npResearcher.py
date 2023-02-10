from app import process_corpora_dataframes
from termcolor import colored

if __name__ == '__main__':
    input_files_dir = input('Введите адрес директории с данными о газетах в формате .json.gz, которые необходимо экспортировать в .xlsx в виде датафреймов: ')
    if len(input_files_dir) == 0:
        print(colored('с данными о газетах в формате .json.gz, которые необходимо экспортировать в .xlsx в виде датафреймов.', 'red'))
        input_files_dir = input('Введите адрес ещё раз, или нажмите Enter, чтобы закрыть программу...')
        
        if len(input_files_dir) == 0:
            exit()
        else:
            process_corpora_dataframes(input_files_dir)
    else:
        process_corpora_dataframes(input_files_dir)
