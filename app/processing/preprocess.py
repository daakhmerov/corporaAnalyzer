import re

def clean_hyphenation(text_on_page:str):
    replace_dict = {
        '-\n':'',
        '- ':'',
    }

    for k in replace_dict.keys():
        text_on_page = text_on_page.replace(k, replace_dict.get(k))

    return text_on_page

def remove_newlines(text_on_page:str):
    text_on_page = re.sub('\n', ' ', text_on_page)

    return text_on_page

def remove_numbers(text_on_page:str):
    return re.sub(r'\d+', '', text_on_page)


def preprocess_text(text_on_page:str):
    # Converting text to lowercase
    text_on_page = text_on_page.lower()

    # Removing hyphenation
    text_on_page = clean_hyphenation(text_on_page)

    # Removing newlines
    text_on_page = remove_newlines(text_on_page)

    # Removing numbers
    text_on_page = remove_numbers(text_on_page)

    return text_on_page