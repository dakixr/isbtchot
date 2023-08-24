import requests
import datetime
import pandas as pd
import isbtchot


CACHE_BTC_PATH = isbtchot.root_path / "cache" / "btc.csv"


def btc_historical_daily() -> pd.DataFrame:
    # Ensure the directory exists
    CACHE_BTC_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Check if the file exists and was modified today
    if (
        CACHE_BTC_PATH.is_file()
        and datetime.datetime.fromtimestamp(CACHE_BTC_PATH.stat().st_mtime).date()
        == datetime.datetime.today().date()
    ):
        df = pd.read_csv(CACHE_BTC_PATH)

    else:
        data = requests.get(
            "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&allData=true"
        ).json()["Data"]["Data"]
        df = pd.DataFrame(data)
        df.to_csv(CACHE_BTC_PATH, index=False)

    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    return df


def btc_pi(months):
    df = btc_historical_daily()[["close"]].rename({"close": "price"}, axis=1)

    df["sma111"] = df["price"].rolling(window=111).mean()
    df["sma350x2"] = df["price"].rolling(window=350).mean() * 2
    df["pi"] = df["sma111"] / df["sma350x2"]

    df = df.drop(["sma111", "sma350x2"], axis=1)
    df = df.dropna()

    # Sell Indicator
    mask_pi_sell = (df["pi"].shift(-1) < 1) & (df["pi"] >= 1)
    df["pi_sell"] = mask_pi_sell

    # Buy indicator
    mask_pi_buy = (df["pi"].shift(-1) > 0.35) & (df["pi"] <= 0.35)
    df["pi_buy"] = mask_pi_buy

    df = df.resample("M").agg(
        {
            "price": "last",
            "pi": "max",
            "pi_sell": "max",
            "pi_buy": "max",
        }
    )

    df = df.reset_index()
    df.time = df.time.dt.strftime("%d/%m/%Y")

    if months:
        df = df.iloc[-months:]

    return df


def btc_monthly(months):
    df = btc_historical_daily()
    df = df.rename(
        {"open": "Open", "close": "Close", "high": "High", "low": "Low"}, axis=1
    )
    df = df.resample("M").agg(
        {
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
        }
    )
    if months:
        df = df.iloc[-months:]
    return df
