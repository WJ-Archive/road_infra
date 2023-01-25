# -*- coding: utf-8 -*-
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# main.py 기준 절대 주소 사용
from config import font_conf


class GraphView(QWidget):
    def __init__(self,  stylesheet="qss/graphWin.qss"):
        super().__init__()

        # 폰트 설정 정의
        FRONT_TYPE = font_conf["type"]["Arial"]
        FRONT_SIZE = font_conf["size"]["default"]
        FONT = QFont(FRONT_TYPE, FRONT_SIZE)

        self.graph = pg.PlotWidget()
        _vbox = QVBoxLayout()

        # 그래프 style 설정
        self.graph.setBackground((34, 40, 49))
        self.graph.setTitle("Category Name")
        self.graph.setLabel("left", "Unit")
        self.graph.setLabel("bottom", "Time(s)")
        self.graph.addLegend()
        self.graph.showGrid(x=True, y=True)
        # self.graph.setMinimumSize(200, 100)

        _vbox.addWidget(self.graph)
        self.setLayout(_vbox)

        self.cbox = QComboBox(self)
        self.cbox.setEditable(True)
        self.cbox.addItem("--")
        self.line_edit = self.cbox.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.3)
        self.cbox.setGraphicsEffect(opacity_effect)
        self.cbox.move(20, 20)
        self.cbox.setFont(FONT)

        # 위젯 크기 및 그 외 설정
        self.setAttribute(Qt.WA_StyledBackground, True)

        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())
