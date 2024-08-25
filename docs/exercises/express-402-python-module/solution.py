import pandas as pd

# This is the non-reactive function:
def filter_weather(data, cities, dates):
    df = data.copy()
    df = df[df["city"].isin(cities)]
    df["date"] = pd.to_datetime(df["date"])
    dates = pd.to_datetime(dates)
    df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
    return df