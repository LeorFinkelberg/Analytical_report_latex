import streamlit as st
import scipy.integrate as integrate
from typing import NoReturn, Tuple
from scipy.special import gamma
import numpy as np
from collections import namedtuple
from helper_functions import text_downloader, prepare_multiline_for_latex


title_app = ("Приложение для расчета усталостной долговечности силовых "
             "элементов транспортных машин")
st.set_page_config(
    layout="wide",
    page_title=title_app,
    initial_sidebar_state="expanded",
)


def spectral_density(
    *,
    alpha: float,
    w0: float,
    s: float,
    w: float,
) -> float:
    """
    Вычисляет спектральную плотность процесса
    """
    W = s ** 2 / (2 * alpha * np.sqrt(np.pi)) * (
        np.exp( -(w + w0) ** 2 / (4 * alpha ** 2) ) +
        np.exp( -(w - w0) ** 2 / (4 * alpha ** 2) )
    )
    
    return W


def lambda1_compute(
    alpha: float,
    w0: float,
    s: float,
) -> float:
    """
    Вычисляет параметр lambda1
    """
    return integrate.quad(
        lambda w: w * spectral_density(alpha=alpha, w0=w0, s=s, w=w),
        0, np.inf)[0]


def lambda_alpha_compute(
    *,
    alpha: float,
    w0: float,
    s_sigma: float,        
) -> Tuple:
    """
    Вычисляет параметры lambda0, lambda1, lambda2, lambda4,
    alpha1, alpha2
    """
    lambda0 = s_sigma ** 2
    lambda1 = lambda1_compute(alpha=alpha, w0=w0, s=s_sigma)
    lambda2 = 2 * alpha ** 2 * s_sigma **2 + s_sigma ** 2 * w0 ** 2
    lambda4 = (
        12 * alpha ** 4 * s_sigma ** 2 +
        12 * alpha ** 2 * s_sigma ** 2 * w0 ** 2 + s_sigma ** 2 * w0 ** 4
    )
    alpha1 = lambda1 / np.sqrt(lambda0 * lambda2)
    alpha2 = lambda2 / np.sqrt(lambda0 * lambda4)
    
    Params = namedtuple("Params", [
        "lambda0", "lambda1", "lambda2", "lambda4", "alpha1", "alpha2"  
    ])
    
    Params.lambda0 = lambda0
    Params.lambda1 = lambda1
    Params.lambda2 = lambda2
    Params.lambda4 = lambda4
    Params.alpha1 = alpha1
    Params.alpha2 = alpha2
    
    return Params
    

def model_miles_compute(
    *,
    alpha: float,
    w0: float,
    sigma_minusd: float,
    s_sigma: float,
    m: float,
    N0: float,
) -> float:
    """
    Вычисляет оценку усталостной долговечности
    по модели Miles
    """
    params = lambda_alpha_compute(alpha=alpha, w0=w0, s_sigma=s_sigma)
    v0 = 1/(2 * np.pi) * np.sqrt( params.lambda2 / params.lambda0 )
    C = sigma_minusd ** m * N0
    Y_NB = ( v0 / C * ( np.sqrt(2) * s_sigma ) ** m * gamma(1 + m / 2) )**(-1)
    
    return Y_NB


def model_wirsch_light_compute(
    *,
    alpha: float,
    w0: float,
    sigma_minusd: float,
    s_sigma: float,
    m: float,
    N0: float,
) -> float:
    """
    Вычисляет оценку усталостной долговечности
    по модели Wirsching-Light
    """
    params = lambda_alpha_compute(alpha=alpha, w0=w0, s_sigma=s_sigma)
    
    epsilon = np.sqrt(1 - params.alpha2 ** 2)
    a0 = 0.926 - 0.033 * m
    b0 = 1.587 * m - 2.323
    hi_WL = a0 + (1 - a0) * (1 - epsilon) ** b0
    
    Y_WL = hi_WL ** (-1) * model_miles_compute(
        alpha=alpha, w0=w0, s_sigma=s_sigma,
        sigma_minusd=sigma_minusd, m=m, N0=N0
    )
    
    return Y_WL


def model_tovo_benasciutti_compute(
    *,
    alpha: float,
    w0: float,
    sigma_minusd: float,
    s_sigma: float,
    m: float,
    N0: float,
) -> float:
    """
    Вычисляет оценку усталостной долговечности
    по модели Tovo-Benasciutti
    """
    params = lambda_alpha_compute(alpha=alpha, w0=w0, s_sigma=s_sigma)
    
    b_app = (1.112 * (1 + params.alpha1 * params.alpha2 - (params.alpha1 + params.alpha2)) *
             np.exp(2.110 * params.alpha2) + (params.alpha1 - params.alpha2) ) * (params.alpha1 - params.alpha2) / (params.alpha2 - 1) ** 2
    
    Y_NB = model_miles_compute(
        alpha=alpha, w0=w0, sigma_minusd=sigma_minusd,
        s_sigma=s_sigma, m=m, N0=N0
    )
    
    D_NB = Y_NB ** (-1)
    
    D_RC = D_NB * params.alpha2 ** (m - 1)
    Y_TB = ( b_app * D_NB + (1 - b_app) * D_RC ) ** (-1)
    
    return Y_TB


def input_params() -> NoReturn:
    """
    Вычисляет оценки усталостной долговечности по различными моделям и
    возвращает общий LaTeX-шаблон
    """
    st.sidebar.subheader("Общие сведения")
    author = st.sidebar.text_input(
        "Автор работы",
        value = "Иванов И.И."
    )
    title = st.sidebar.text_area(
        "Заголовок отчета",
        value = (
            "Аналитический отчет по оценке усталостной долговечности "
            "силовых элементов транспортных машин под воздействием "
            "стационарных гауссовских процессов"
        )
    )
    st.sidebar.subheader("Параметры моделей")
    alpha = st.sidebar.number_input(
        ("Параметр alpha модели случайного процесса с автокорреляционной функцией "
         "экспоненциально-косинусного типа"),
        value=3.0,
        min_value=1.0,
        max_value=100.0,
        format="%f"  
    )
    w0 = st.sidebar.number_input(
        ("Параметр w0 модели случайного процесса с автокорреляционной функцией "
         "экспоненциально-косинусного типа"),
        value=55.0,
        min_value=1.0,
        max_value=100.0,
        format="%f"  
    )
    N0 = st.sidebar.number_input(
        "Абсцисса точки перегиба кривой выносливости",
        value=1.3*10**6,
        min_value=1.0*10**4,
        max_value=1.0*10**8,
        format="%f"
    )
    sigma_minusd = st.sidebar.number_input(
        "Предел выносливости детали, [МПа]",
        value=85.0,
        min_value=10.0,
        max_value=100.0,
        format="%f"
    )
    m = st.sidebar.number_input(
        "Тангенс угла наклона левой ветви кривой выносливости",
        value=4.0,
        min_value=1.0,
        max_value=6.0,
        format="%f"
    )
    s_sigma = st.sidebar.number_input(
        "Стандартное отклонение процесса, [МПа]",
        value = 100.0,
        min_value = 10.0,
        max_value = 200.0,
        format="%f"
    )
    
    params = dict(
        alpha=alpha, w0=w0, s_sigma=s_sigma,
        m=m, sigma_minusd=sigma_minusd, N0=N0
    )
    
    Y_NB = model_miles_compute(**params)
    Y_WL = model_wirsch_light_compute(**params)
    Y_TB = model_tovo_benasciutti_compute(**params)
    
    template_for_latex: str = prepare_multiline_for_latex(
        title=title, author=author, Y_NB=Y_NB, Y_WL=Y_WL, Y_TB=Y_TB
    )
    text_downloader(template_for_latex)


def header() -> NoReturn:
    """
    Выводит на странице заголовки главной и боковой панелей
    """
    st.title(title_app)
    st.sidebar.header("Входные данные")
    
    
def order_of_actions():
    """
    Выводит на главной странице порядок работы
    с приложением
    """
    st.markdown("### Порядок работы с приложением:")
    st.markdown("_1. Задать значения управляющих параметров приложения_")
    st.markdown(
        "_2. Скачать подготовленный tex-файл (```base_template_for_latex.tex```) "
        "в рабочую директорую проекта, кликнув по 'Скачать опорный tex-файл ...'_"
    )
    st.markdown("_3. Запустить в рабочей директории проекта компилятор (дважды!)_")
    st.code("""
# для сборки каркаса
$ pdflatex base_template_for_latex.tex
# для вычисления конечных ссылок на страницы, формулы и пр.
$ pdflatex base_template_for_latex.tex
    """, language="bash")
    st.markdown("_4. Ознакомиться с результатами работы LaTeX_")


if __name__ == "__main__":
    header()
    order_of_actions()
    input_params()