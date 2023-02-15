def welcome_page():
    # Импорт необходимых библиотек
    from termcolor import colored
    from app import __version__, name, description

    # Вспомогательные функции
    def dec_len(char):
        return char * (len(f'{__version__}{name}') + 1)
        
    # Определение функций
    def launch():
        from app.project.project import Project

        project_dir = input(colored(
            'Введите путь к проекту, или нажмите Enter, чтобы закрыть программу: ', 'cyan'))
        if project_dir == '':
            exit()
        else:
            try:
                Project(project_dir).analyze()
            except FileNotFoundError as f_e:
                print(
                    colored(f'Не удается найти указанный путь. Попробуйте снова: ', 'red'))
                launch()
            except Exception as e:
                print(colored(f'Ошибка!\n{e}\n', 'red'))
                if input('Нажмите Enter, чтобы закрыть программу...'):
                    exit()

    print(colored(f'{dec_len("=")} {name} {__version__} {dec_len("=")}', 'magenta'))
    launch()