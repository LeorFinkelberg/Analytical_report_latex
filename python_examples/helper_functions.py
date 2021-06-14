import base64
import logging
import sys
from typing import NoReturn
import streamlit as st
from pathlib2 import Path


def make_stream_handler() -> logging.FileHandler:
    """
    Настравивает потоковый хендлер
    """
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def make_logger(logger_name: str) -> logging.Logger:    
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(make_stream_handler())
    return logger


_log_format = "[%(asctime)s | %(levelname)s]: %(message)s"
logger = make_logger(__name__)


def text_downloader(multiline: str) -> NoReturn:
    """
    Принимает LaTeX-шаблон документа в виде многострочной строки и
    создает на странице ссылку для скачивания шаблона
    """
    OUTPUT_TEX_FILENAME = "base_template_for_latex.tex"
    
    b64 = base64.b64encode(multiline.encode()).decode()
    # создает ссылку для скачивания файла
    href = (f'<a href="data:file/txt;base64,{b64}" '
            f'download="{OUTPUT_TEX_FILENAME}">Скачать опорный tex-файл для сборки аналитического отчета в LaTeX</a>')
    st.markdown(href, unsafe_allow_html=True)


def prepare_multiline_for_latex(
    *,
    title: str,
    author: str,
    Y_NB: float,
    Y_WL: float,
    Y_TB: float,
) -> str:
    """
    Читает txt-загатовку для LaTeX и возвращает подготовленный LaTeX-шаблон
    в виде строки
    """
    WORK_DIR = Path("python_examples").absolute()
    LATEX_TEMPLATE_FILENAME = "latex_template_for_python.txt" # <-- NB: txt, а не tex
    LATEX_TEMPLATE_PATH = WORK_DIR.joinpath(Path(LATEX_TEMPLATE_FILENAME))

    try:
        with open(LATEX_TEMPLATE_PATH, encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError as err:
        logger.error(err)
    except FileExistsError as err:
        logger.error(err)

    return template.format(
        title=title,
        author=author,
        Y_NB=Y_NB,
        Y_WL=Y_WL,
        Y_TB=Y_TB
    )


if __name__ == "__main__":
    print("Этот вспомогательный модуль. Его не нужно запускать напрямую")