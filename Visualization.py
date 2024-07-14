#! ./.venv/bin/python

from typing import Any
import plotly.graph_objects as go
import plotly.express as px
from DataBase import DataBase
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from indicator import moving_Averages


class Visualization:
    def __init__(self) -> None:
        self.fig = make_subplots(rows=2, cols=1,
                                 shared_xaxes=True,
                                 vertical_spacing=0.02,
                                 row_heights=[0.8, 0.2])

    def Candlestick(self, data: pd.DataFrame):
        candlestick = go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'], name="Candlestick"
                                     )
        self.fig.add_trace(candlestick, row=1, col=1)
        # self.fig = go.Figure(candlestick)
        self.fig.update_layout(xaxis_rangeslider_visible=False)

    def Volome(self, data: pd.DataFrame) -> None:
        color = np.where(data["Open"] <= data["Close"], "green", "red")
        color = np.where(data["Open"] == data["Close"], "yellow", color)
        bar_chart = go.Bar(
            x=data.index,
            y=data['Volume'],
            marker=dict(
                color=color),
            name="Volume")

        self.fig.add_trace(bar_chart, row=2, col=1)

    def Moving_Average(
            self,
            data: pd.DataFrame,
            window=5,
            Colomn: str = "Close", simple=True) -> None:
        mv = moving_Averages(data[Colomn], window=window, simple=simple)
        name = "Simple" if simple else "Exponential"

        mv_chart = go.Scatter(
            x=mv.index,
            y=mv,
            mode="lines",
            name=f"{name} Moving Average {window}"
        )
        self.fig.add_trace(mv_chart, row=1, col=1)

    def show(self) -> None:
        self.fig.show()

    def write_html(
            self,
            path: str = '.cache/chart.html',
            auto_open: bool = True) -> None:
        self.fig.write_html(file=path, auto_open=auto_open)


if __name__ == "__main__":

    sql = DataBase()
    table = "MSFT"
    column = "Date"
    start = "2024-02-28"
    end = "2024-07-03"

    data = sql.select_data(table, start=start, end=end)
    v = Visualization()
    v.Candlestick(data=data)
    v.Volome(data=data)
    v.Moving_Average(data=data)
    # v.show()
    v.write_html()
