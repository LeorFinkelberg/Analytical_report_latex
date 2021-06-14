import base64
from typing import NoReturn
import streamlit as st


def text_downloader(multiline: str) -> NoReturn:
    """
    Принимает LaTeX-шаблон документа в виде многострочной строки и
    создает на форме ссылку для скачивания шаблона
    """
    OUTPUT_TXT_FILENAME = "base_template_for_latex.tex"
    
    b64 = base64.b64encode(multiline.encode()).decode()
    st.markdown("#### Download File ####")
    href = (f'<a href="data:file/txt;base64,{b64}" '
            f'download="{OUTPUT_TXT_FILENAME}">Скачать LaTeX-файл</a>')
    st.markdown(href, unsafe_allow_html=True)


def prepare_multiline_for_latex(
    *,
    title: str,
    author: str,
    Y_NB: float,
) -> NoReturn:
    template = f"""
\\documentclass{{article}}

\\usepackage{{style_template}}

\\begin{{document}}

\\title{{ {title} }} % заголовок отчета
\\author{{\\itshape {author} }} % имя автора работы
\\date{{}} % просим LaTeX не указывать дату, так как будет
% использован наш вариант оформления даты, описанный в стилевом файле
\\maketitle % создать заголовок

\\thispagestyle{{fancy}} % задает стиль страницы

\\tableofcontents

\\section{{Оценка УСТАЛОСТНОЙ долговечности по модели J.W. Miles}}

Модель Miles \\cite{{miles-1954}}, строго говоря, применима только к узкополосным случайным процессам (процессам с узким энергетическим спектром), поэтому при нагружении широкополосными процессами модель дает слишком консервативные оценки

\\begin{{align}}\\label{{eq:miles}}
	Y_{{NB}}(s_{{\\sigma}}) = \\Big[ \\, \\dfrac{{f}}{{C}} \\, ( \\sqrt{{2}} s_{{\\sigma}} )^m \\, \\Gamma \\bigg( 1 + \\dfrac{{m}}{{2}} \\bigg) \\, \\Big]^{{-1}}, \\ C = \\sigma_{{-1\\text{{д}}}}^m N_0,
\\end{{align}}
где $ f $ -- эффективная частота случайного процесса, Гц; $ \\sigma_{{-1\\text{{д}}}} $ -- предел выносливости детали, МПа; $ s_{{\\sigma}} $ -- стандартное отклонение случайного процесса, МПа; $ m $ -- тангенс угла наклона левой ветви кривой выносливости; $ \\Gamma(\\cdot) $ -- гамма-функция.

Усталостная долговечность по модели \\eqref{{eq:miles}} составляет $ Y_{{NB}} = {Y_NB:.2f} $, сек.

\\begin{{thebibliography}}{{99}}\\addcontentsline{{toc}}{{section}}{{Список литературы}}
	\\bibitem{{miles-1954}}{{\\emph{{Miles J.W.}} On structural fatigue under random loading // Journal Aueronaut Science. 1954. V. 21. P. 753 -- 762.}}
\\end{{thebibliography}}

\\end{{document}}
""".strip()

    text_downloader(template)