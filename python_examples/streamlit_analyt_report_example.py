import streamlit as st

from typing import NamedTuple
from scipy.special import gamma
import math
from helper_functions import prepare_multiline_for_latex


title_app = ("Приложение для расчета усталостной долговечности силовых "
             "элементов транспортных машин")
st.set_page_config(
    layout="wide",
    page_title=title_app,
    initial_sidebar_state="expanded",
)
    

def model_miles_compute(
    *,
    f: float,
    sigma_minusd: float,
    s_sigma: float,
    m: float,
    N0: float,
) -> float:
    """
    Вычисляет оценку усталостной долговечности по модели Miles
    """
    C = sigma_minusd ** m * N0
    Y_NB = ( f / C * ( math.sqrt(2) * s_sigma ) ** m * gamma(1 + m / 2) )**(-1)
    
    return Y_NB


def model_wirsch_light_compute():
    pass


def model_zhao_baker_compute():
    pass


def model_tovo_bensciutti_compute():
    pass


def input_params(
    title: str,
    author: str,
) -> NamedTuple:
    """
    Вычисляет оценки усталостной долговечности по различными моделям и
    возвращает общий LaTeX-шаблон
    """
    N0 = st.sidebar.number_input(
        "Абсцисса точки перегиба кривой выносливости",
        value=1.3*10**6,
        min_value=1.0*10**4,
        max_value=1.0*10**8,
        format="%f"
    )
    sigma_minusd = st.sidebar.number_input(
        "Предел выносливости детали, [МПа]",
        value=85,
        min_value=10,
        max_value=100,
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
        value = 100,
        min_value = 10,
        max_value = 200,
        format="%f"
    )
    
    f = st.sidebar.number_input(
        "Эффективная частота процесса, [Гц]",
        value = 8.78,
        min_value = 1.0,
        max_value = 100.0,
        format="%f"
    )
    
    Y_NB = model_miles_compute(f=f, s_sigma=s_sigma, m=m, sigma_minusd=sigma_minusd, N0=N0)
    
    st.write(Y_NB)
    prepare_multiline_for_latex(title=title, author=author, Y_NB=Y_NB)


if __name__ == "__main__":
    st.title(title_app)
    
    st.sidebar.header("Входные данные")
    
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
    
    input_params(title, author)
    
    if st.button("Собрать pdf-документ"):
        pass
