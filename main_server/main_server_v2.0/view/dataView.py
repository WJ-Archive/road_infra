# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# main.py 기준 절대 주소 사용
from config import win_conf, font_conf

from config import info_btn
from packages.utils.btn import InfoBtn


class DataView(QWidget):
    def __init__(self, stylesheet="qss/dataWin.qss"):
        super().__init__()

        # 위젯 크기 정의
        MIN_WIN_WIDTH = win_conf["data_view"]["min_width"]
        MIN_WIN_HEIGHT = win_conf["data_view"]["min_height"]

        # 버튼 생성
        self.temp_info_btn = InfoBtn(info_btn[0])
        self.humid_info_btn = InfoBtn(info_btn[1])
        self.illum_info_btn = InfoBtn(info_btn[2])
        self.acc_info_btn = InfoBtn(info_btn[3])
        self.pothole_info_btn = InfoBtn(info_btn[4])

        # 뷰 배치
        _grid_layout = QGridLayout()

        _grid_layout.addWidget(self.temp_info_btn, 0, 0)
        _grid_layout.addWidget(self.humid_info_btn, 0, 1)
        _grid_layout.addWidget(self.illum_info_btn, 0, 2)
        _grid_layout.addWidget(self.pothole_info_btn, 1, 0)
        _grid_layout.addWidget(self.acc_info_btn, 1, 1, 1, 2)

        self.setLayout(_grid_layout)

        # 위젯 크기 설정
        self.setMinimumSize(MIN_WIN_WIDTH, MIN_WIN_HEIGHT)

        # 위젯 백그라운드 적용 유무 확인
        self.setAttribute(Qt.WA_StyledBackground, True)

        # qss 적용
        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())
