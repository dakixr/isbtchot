from isbtchot import model
from isbtchot import view as v
from isbtchot.schemas.args import TypeTime


view = v.ViewPlotText()

def btc_terminal(time_grouping: TypeTime, periods_back: int):
    df = model.btc_hist(time_grouping, periods_back)
    view.candle_stick_terminal(df, "BTC/USD")
    view.plt.yscale("log")

def btc_pi_terminal(time_grouping: TypeTime, periods_back):
    df = model.btc_pi(time_grouping, periods_back)
    view.chart_terminal(df.time, df.pi, "Hotness Index")
    view.add_horizontal_line(1, "red")
    view.add_horizontal_line((0.95 - 0.35) / (1 - 0.35), "red")
    view.add_horizontal_line((0.80 - 0.35) / (1 - 0.35), "orange")
    view.add_horizontal_line((0.66 - 0.35) / (1 - 0.35), "green")
    view.add_horizontal_line(0, "blue")
    for _, row in df.iterrows():
        if row.pi_sell:
            view.add_vertical_line(row.time, "red")
        if row.pi_buy:
            view.add_vertical_line(row.time, "green")
    view.plt.ylim(df.pi.min(), max(1, df.pi.max()))
    

def dashboard(time_grouping: TypeTime, periods_back: int):
    view.dimensions(0, -4)
    view.subplots(2,1)
    view.select_subplot(1,1)
    btc_terminal(time_grouping, periods_back)
    view.select_subplot(2,1)
    btc_pi_terminal(time_grouping, periods_back)
    view.show()