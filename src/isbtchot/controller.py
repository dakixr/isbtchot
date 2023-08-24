from isbtchot import model
from isbtchot import view as v

view = v.ViewPlotText()

def btc_terminal(months):
    df = model.btc_monthly(months)
    view.candle_stick_terminal(df, "BTC/USD")
    view.plt.yscale("log")

def btc_pi_terminal(months):
    df = model.btc_pi(months)
    view.chart_terminal(df.time, df.pi, "Hotness Index")
    view.add_horizontal_line(1, "red")
    view.add_horizontal_line(0.35, "green")
    for _, row in df.iterrows():
        if row.pi_sell:
            view.add_vertical_line(row.time, "red")
        if row.pi_buy:
            view.add_vertical_line(row.time, "green")
    view.plt.ylim(0.20, 1.1)
    

def dashboard(months=None):
    view.dimensions(0, -4)
    view.subplots(2,1)
    view.select_subplot(1,1)
    btc_terminal(months)
    view.select_subplot(2,1)
    btc_pi_terminal(months)
    view.show()