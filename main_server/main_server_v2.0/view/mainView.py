# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import Qt, pyqtSignal

# main.py 기준 절대 주소 사용
from view.videoView import VideoView
from view.dataView import DataView
from view.gpsView import GpsView
from view.graphView import GraphView
from view.logView import LogView
from view.dataSearchView import DataSearchView


class MainView(QWidget):
    signal = pyqtSignal(int, int)

    def __init__(self, stylesheet="qss/mainWin.qss"):
        super().__init__()

        # 레이아웃 선언
        _grid_layout = QGridLayout()
        _vbox = QVBoxLayout()
        _hbox = QHBoxLayout()

        # 화면 선언
        self.data_view = DataView()     # 데이터 화면
        self.video_view = VideoView()   # 운전 화면
        self.gps_view = GpsView()       # GPS 화면
        self.log_view = LogView()       # Log 화면
        self.graph_view = GraphView()   # 그래프 화면
        self.data_search_view = DataSearchView() # DB 조회 화면

        # 위젯 배치
        _grid_layout.addWidget(self.video_view, 0, 0)
        _grid_layout.addWidget(self.gps_view, 0, 1)
        _grid_layout.addWidget(self.data_search_view, 0, 2)
        _grid_layout.addWidget(self.data_view, 1, 0)
        _grid_layout.addWidget(self.graph_view, 1, 1)
        _grid_layout.addWidget(self.log_view, 1, 2)
        _grid_layout.setColumnStretch(0, 2) # 인자(컬럼, 컬럼 스펜)
        _grid_layout.setColumnStretch(1, 3)
        _grid_layout.setColumnStretch(2, 2)
        _grid_layout.setRowStretch(0, 3)
        _grid_layout.setRowStretch(1, 1)


        _hbox.addLayout(_grid_layout)
        _hbox.addLayout(_vbox)

        self.setLayout(_hbox)

        with open(stylesheet, "r") as file:
            self.setAttribute(Qt.WA_StyledBackground, True)
            self.setStyleSheet(file.read())


    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        resize Event connected with pyqtsingal
        """
        self.signal.emit(self.geometry().width(), self.geometry().height())

