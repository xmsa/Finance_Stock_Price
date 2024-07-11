#! ./.venv/bin/python

from typing import Any
import plotly.graph_objects as go
import plotly.express as px
from DataBase import DataBase


class Visualization:
    def __init__(self) -> None:
        pass

    def Candlestick(self, data):
        candlestick = go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close']
                                     )
        self.fig = go.Figure(candlestick)
        self.fig.update_layout(xaxis_rangeslider_visible=False)

    def show(self):
        self.fig.show()

    def write_html(self, auto_open=True):
        self.fig.write_html('.cache/chart.html', auto_open=auto_open)


if __name__ == "__main__":

    sql = DataBase()
    table = "MSFT"
    column = "Date"
    data = sql.select_data(table, start="2024-05-28", end="2024-07-03")

    v = Visualization()
    v.Candlestick(data=data)
    # v.show()
    v.write_html()
