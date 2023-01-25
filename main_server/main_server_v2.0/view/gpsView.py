# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

from view.timeAndPosView import TimeAndPosView


class GpsView(QWidget):
    def __init__(self, stylesheet="qss/gpsWin.qss"):
        super().__init__()

        # 시간, 위치 정보 view 생성
        self.time_pos_view = TimeAndPosView()
        # self.time_pos_view = None

        # gps view 생성
        self.map_view = QWebEngineView(self, objectName="gps_lb")

        # 레이블을 GPS 위젯에 고정
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.time_pos_view, 1)
        self.vbox.addWidget(self.map_view, 9)
        self.setLayout(self.vbox)

        # GPS 위젯 설정
        self.setAttribute(Qt.WA_StyledBackground, True)

        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())



