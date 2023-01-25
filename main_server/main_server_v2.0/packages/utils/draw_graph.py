from PyQt5.QtCore import QThread
import pyqtgraph as pg


class DrawGraph(QThread):
    def __init__(self, data_queue):
        super().__init__()
        self._graph = pg.PlotWidget()
        self._x = []
        self._y = []
        self._data_q = data_queue
        self._cnt = 0
        self._time_limit = 100

        # style 설정
        self._graph.setBackground('w')
        self._graph.setTitle("Title")
        self._graph.setLabel("left", "y-axis")
        self._graph.setLabel("bottom", "x-axis")
        self._graph.addLegend()
        self._graph.showGrid(x=True, y=True)

    def run(self):
        self._graph.clear()
        if self._cnt > self._time_limit:
            self._cnt = 0
            self._x = []
            self._y = []

            self._cnt += 1
            self._x.append(self._cnt)
            a = self._data_q.get()
            print(a)
            self._y.append(a)
            self.graph.plot(x=self._x, y=self._y, pen=pg.mkPen(width=2, color='r'))
