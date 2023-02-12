def _get_bigrams(token_index, tokens):
    if token_index > 0 and token_index < len(tokens) - 1:
        return [
            tokens[token_index-1:token_index+1],
            tokens[token_index:token_index+2]
        ]
    elif token_index == 0:
        return [tokens[token_index:token_index+2]]
    else:
        return [tokens[token_index-1:token_index+1]]


def sent_tokenize_text(text_on_page):
    from nltk import sent_tokenize

    return sent_tokenize(text_on_page, language='russian')


def word_tokenize_text(text_on_page: str):
    from nltk import word_tokenize
    import string

    text_tokens = []
    sentences = sent_tokenize_text(text_on_page)

    for sent in sentences:
        tokens = [token for token in word_tokenize(
            sent, language='russian') if token not in string.punctuation]
        for index, token in enumerate(tokens):
            text_tokens.append(
                {'token': token, 'bigrams': _get_bigrams(index, tokens)})
    return text_tokens
