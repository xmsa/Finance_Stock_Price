import pandas as pd


def moving_Averages(data: pd.Series, window: int = 5, simple: bool = True):
    if simple:
        return data.rolling(window=window).mean()
    return data.ewm(span=window, adjust=False).mean()
