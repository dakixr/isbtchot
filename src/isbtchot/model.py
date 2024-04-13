import numpy as np
import requests
import datetime
import pandas as pd
import isbtchot
from isbtchot.schemas.args import TypeTime
from sklearn.linear_model import LinearRegression


CACHE_BTC_PATH = isbtchot.root_path / "cache" / "btc.csv"
BTC_API = (
    "https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&allData=true"
)


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

    # Fetch new data
    else:
        try:
            data = requests.get(BTC_API).json()["Data"]["Data"]

        except Exception as _:
            # Try without ssl enabled
            data = requests.get(BTC_API, verify=False).json()["Data"]["Data"]

        df = pd.DataFrame(data)
        df.to_csv(CACHE_BTC_PATH, index=False)

    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    return df


def btc_pi(time_grouping: TypeTime, periods_back: int | None = None):
    df = btc_historical_daily()[["close"]].rename({"close": "price"}, axis=1)

    df["sma111"] = df["price"].rolling(window=111).mean()
    df["sma350x2"] = df["price"].rolling(window=350).mean() * 2
    df["pi"] = df["sma111"] / df["sma350x2"]

    df = df.drop(["sma111", "sma350x2"], axis=1)
    df = df.dropna()

    # Normalize pi
    df["pi"] = (df["pi"] - 0.35) / (1 - 0.35)

    # Sell Indicator
    mask_pi_sell = (df["pi"].shift(-1) >= 1) & (df["pi"] < 1)
    df["pi_sell"] = mask_pi_sell

    # Buy indicator
    mask_pi_buy = (df["pi"].shift(-1) <= 0) & (df["pi"] > 0)
    df["pi_buy"] = mask_pi_buy

    df = df.resample(time_grouping.value).agg(
        {
            "price": "last",
            "pi": "max",
            "pi_sell": "max",
            "pi_buy": "max",
        }
    )

    df = df.reset_index()
    df.time = df.time.dt.strftime("%d/%m/%Y")

    if periods_back:
        periods_back = min(periods_back, len(df))
        df = df.iloc[-periods_back:]

    return df


def btc_hist(time_grouping: TypeTime | None = None, periods_back: int | None = None):
    df = btc_historical_daily()
    df = df.rename(
        {"open": "Open", "close": "Close", "high": "High", "low": "Low"}, axis=1
    )
    if time_grouping:
        df = df.resample(time_grouping.value).agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
            }
        )
    if periods_back:
        df = df.iloc[-periods_back:]
    return df


def btc_power_law(
    time_grouping: TypeTime | None = None,
    periods_back: int | None = None,
    years_to_predict: int = 20,
) -> pd.DataFrame:
    df = btc_hist(time_grouping=time_grouping)[["Close"]].rename(
        {"Close": "price"}, axis=1
    )

    # Adjust for genesis block
    genesis_delta = (df.index[0] - pd.Timestamp(year=2009, month=1, day=3)).days
    if time_grouping is TypeTime.WEEK:
        genesis_delta /= 7
    elif time_grouping is TypeTime.MONTH:
        genesis_delta /= 30

    df["days"] = np.arange(len(df)) + genesis_delta
    # Applying log transformation
    X_log = np.log(df["days"].values.reshape(-1, 1))
    y_log = np.log(df["price"].values)

    # Fit the linear regression model on the log-transformed data
    power_law_model = LinearRegression().fit(X_log, y_log)

    # The coefficient 'b' is the slope of the line in the log-log space
    b = power_law_model.coef_[0]
    # The coefficient 'a' is obtained by taking the exponential of the intercept in the log-log space
    a = np.exp(power_law_model.intercept_)

    # Extend df
    periods = 365 * years_to_predict
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "days": np.arange(periods) + df.days.iloc[-1],
                },
                index=pd.date_range(df.index[-1], periods=periods, freq="D"),
            ),
        ]
    )

    # Using the power law model to predict prices across the original range of days
    df["power_law"] = a * (df.days**b)
    df["power_law_bottom"] = df.power_law * 0.45
    df["power_law_top"] = df.power_law * 3
    df["delta"] = df.price / df.power_law

    if periods_back:
        df = df.dropna().iloc[-periods_back:]
    return df
