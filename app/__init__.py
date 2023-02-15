from app.utilities.log import Log, LogString, Error_, Success, Warning
from app.utilities.files import get_file_paths, check_extension
from app.process.tokenize import word_tokenize_text, sent_tokenize_text
from app.process.preprocess import preprocess_text
from app.process.parsemeta import parse_filename, parse_issue_date
from app.project.project import Project
from app.corpora.corpora import Corpora
from app.document.document import Document
from app.launcher.launcher import welcome_page
name = 'corporaAnalyzer'
__version__ = '0.2'
description = 'corporaAnalyzer — программа для анализа корпусов текстов'
