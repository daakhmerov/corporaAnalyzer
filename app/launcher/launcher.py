def welcome_page():
    # Импорт необходимых библиотек
    from termcolor import colored
    from app import __version__, name

    # Вспомогательные функции
    def dec_len(char):
        return char * (len(f'{__version__}{name}') + 1)
    # Определение функций

    def launch():
        from app.analyzing.analyze import analyze_project

        project_dir = input(colored(
            'Введите путь к проекту, или нажмите Enter, чтобы закрыть программу: ', 'cyan'))
        if project_dir == '':
            exit()
        else:
            try:
                def ask_gen():
                    ask = input('Нужно ли сгенерировать единые датафреймы по каждому корпусу? Д\н: ').lower()
                    if  ask == 'д' or ask == 'y':
                        analyze_project(project_dir)
                    elif ask == 'н' or ask == 'n':
                        analyze_project(project_dir, generate_df=False)
                    else:
                        print(
                            colored(f'Попробуйте снова: ', 'red'))
                        ask_gen()

                ask_gen()
            except FileNotFoundError as f_e:
                print(
                    colored(f'Не удается найти указанный путь. Попробуйте снова: ', 'red'))
                launch()
            except Exception as e:
                print(colored(f'Ошибка!\n{e}\n', 'red'))
                if input('Нажмите Enter, чтобы закрыть программу...'):
                    exit()

    print(colored(
        f'{dec_len("=")}\nNewspaperAnalyzer {__version__}\n{dec_len("=")}', 'magenta'))
    launch()
