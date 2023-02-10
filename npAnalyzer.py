from app import process_corpora
from termcolor import colored

if __name__ == '__main__':
    input_files_dir = input('Введите адрес директории с газетами, которые необходимо проанализировать: ')
    if len(input_files_dir) == 0:
        print(colored('Вы не ввели адрес директории с газетами, которые необходимо проанализировать.', 'red'))
        input_files_dir = input('Введите адрес ещё раз, или нажмите Enter, чтобы закрыть программу...')
        
        if len(input_files_dir) == 0:
            exit()
        else:
            process_corpora(input_files_dir=input_files_dir)
    else:
        process_corpora(input_files_dir=input_files_dir)