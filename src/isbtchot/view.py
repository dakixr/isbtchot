import plotext as plt
plt.theme('pro')

class ViewPlotText():

    def __init__(self) -> None:
        self._subplots = None

    @property
    def plt(self):
        if not self._subplots:
            return plt
        row, col = self._subplots
        return plt.subplot(row, col)
        
    def select_subplot(self, row, col):
        if row is None or col is None:
            self._subplots = None
            return
        self._subplots = (row, col)

    def chart_terminal(self, x, y, title):
        self.plt.plot(x, y)
        self.plt.title(title)
        self.plt.yticks([])


    def candle_stick_terminal(self, data, title):
        dates = self.plt.datetimes_to_string(data.index)
        self.plt.candlestick(dates=dates, data=data)
        self.plt.title(title)
        self.plt.yticks([])

    def add_horizontal_line(self, value, color):
        self.plt.hline(value, color=color)

    def add_vertical_line(self, index, color):
        values = [0,1]
        idx = [index, index]
        self.plt.plot(idx, values, color=color)

    def dimensions(self, w, h):
        self.plt.plotsize(w + plt.tw(), plt.th() + h)

    def show(self):
        plt.show()

    def subplots(self, rows, cols):
        self.plt.subplots(rows, cols)
