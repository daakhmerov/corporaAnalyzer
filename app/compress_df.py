import pandas

def export_compress_df(df:pandas.core.frame.DataFrame, output:str):
    # Импорт необходимых модулей
    import gzip
    import tempfile

    # Обработка данных
    with tempfile.TemporaryFile() as excel_f:
        df.to_excel(excel_f, index=False)
        with gzip.open(output, 'wb+') as gzip_f:
            excel_f.seek(0)
            gzip_f.write(excel_f.read())