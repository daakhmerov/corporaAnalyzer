name = 'NewspaperAnalyzer'
__version__ = '0.1'

from app.processing.process_corpora import process_corpora
from app.processing.preprocess import preprocess_text
from app.processing.tokenize import word_tokenize_text,sent_tokenize_text
from app.parsing.parsename import parse_filename
from app.processing.process import process_newspaper
from app.utilities.check import check_pdf_file
from app.utilities.log import log_to_html, log_to_json, LogString
from app.parsing.parsemeta import parse_issue_date
from app.processing_data.process_data import tokens_to_df
from app.processing.process_corpora_dataframes import process_corpora_dataframes
from app.processing_data.concat_datasets import concat_datasets
from app.processing_data.pipeline import pipeline
from app.utilities.clean import delete_dir
from app.analyzing.analyze import analyze_project
from app.launcher.launcher import welcome_page