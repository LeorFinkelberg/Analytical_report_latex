import streamlit as st
import math
import pandas as pd
from pandas import Series
import plotly.graph_objects as go
import numpy as np
import numpy.random as rnd

title_app = "Простой пример использования библиотеки Streamlit"
st.set_page_config(
    layout="wide",
    page_title=title_app,
    initial_sidebar_state="expanded",
)


def gauss_with_exp_acf_gen(
    *,
    sigma: float = 2,
    w_star: float = 1.25,
    delta_t: float = 0.05,
    N: int = 1000,
) -> np.array:
    """
    Описание
    --------
    Генерирует дискретную реализацию
    стационарного гауссовского ПСП
    с КФ экспоненциального типа

    Параметры
    ---------
    sigma : стандартное отклонение ординат ПСП.
    w_star : параметр модели ПСП.
    delta_t : шаг по времени.
    N : число отсчетов ПСП.

    Возвращает
    ----------
    xi : массив элементов ПСП с заданной КФ
    """
    gamma_star = w_star * delta_t
    rho = math.exp(-gamma_star)
    b1 = rho
    a0 = sigma * math.sqrt(1 - rho ** 2)

    xi = np.zeros(N)
    xi[0] = rnd.rand()
    x = rnd.randn(N)

    for n in range(1, N):
        xi[n] = a0 * x[n] + b1 * xi[n - 1]

    return xi


def main(N: int = 100):
    timestmp = np.arange(N)
    # временной ряд №1
    time_series_1 = gauss_with_exp_acf_gen(sigma=5, w_star=1.25, N=N)
    # временной ряд №2
    time_series_2 = gauss_with_exp_acf_gen(sigma=6.5, w_star=1.75, N=N)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=timestmp,
            y=time_series_1,
            name="Временной ряд (объект-1)",
            opacity=0.8,
            mode="lines",
            line=dict(
                color="#E84A5F",
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=timestmp,
            y=Series(time_series_1).rolling(window=7).mean(),
            name="Скользящее среднее (объект-1)",
            mode="lines",
            opacity=0.6,
            line=dict(
                color="#FF847C",
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=timestmp,
            y=time_series_2,
            name="Временной ряд (объект-2)",
            mode="lines",
            opacity=0.8,
            line=dict(
                color="#5E63B6",
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=timestmp,
            y=Series(time_series_2).rolling(window=7).mean(),
            name="Скользящее среднее (объект-2)",
            mode="lines",
            opacity=0.6,
            line=dict(
                color="#6EB6FF",
            ),
        )
    )

    fig.update_layout(
        title=dict(
            # text="<i>Временной ряд</i>",
            font=dict(
                family="Arial",
                size=18,
                color="#07689F",
            ),
        ),
        xaxis_title=dict(
            text="<i>Временная метка</i>",
            font=dict(
                family="Arial",
                size=13,
                color="#537791",
            ),
        ),
        yaxis_title=dict(
            text="<i>Продолжительность простоя, час</i>",
            font=dict(
                family="Arial",
                size=13,
                color="#537791",
            ),
        ),
        xaxis=dict(
            showline=True,
        ),
        yaxis=dict(
            showline=True,
        ),
        autosize=False,
        showlegend=True,
        margin=dict(
            autoexpand=False,
            l=70,
            r=10,
            t=50,
        ),
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.01,
            xanchor="right",
            x=0.99,
            font=dict(family="Arial", size=12, color="black"),
        ),
        plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main(N=350)
