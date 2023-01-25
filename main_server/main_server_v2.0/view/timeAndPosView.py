# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QLabel, QLCDNumber, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# main.py 기준 절대 주소 사용
from config import win_conf, font_conf

class TimeAndPosView(QWidget):
    def __init__(self, stylesheet="qss/timeAndPosWin.qss"):
        super().__init__()

        # 폰트 정의 및 설정
        FONT_TYPE = font_conf["type"]["Arial"]
        FONT_SIZE = font_conf["size"]["small"]
        VAL_FONT = QFont(FONT_TYPE, FONT_SIZE)
        TXT_FONT = QFont(FONT_TYPE, FONT_SIZE)
        TXT_FONT.setBold(True)

        # label 및 lcd 생성
        self.time_txt_lb = QLabel("시간", objectName="time_txt_lb")
        self.time_val_lb = QLCDNumber(objectName="time_val_lb")
        self.time_val_lb.display("")
        self.time_val_lb.setDigitCount(20)

        self.lat_txt_lb = QLabel("위도", objectName="lat_txt_lb")
        self.lat_val_lb = QLCDNumber(objectName="lat_val_lb")
        self.lat_val_lb.display("")
        self.lat_val_lb.setDigitCount(10)

        self.long_txt_lb = QLabel("경도", objectName="long_txt_lb")
        self.long_val_lb = QLCDNumber(objectName="long_val_lb")
        self.long_val_lb.display("")
        self.long_val_lb.setDigitCount(10)

        # time screen 병합
        _time_hbox = QHBoxLayout()
        _latlon_hbox = QHBoxLayout()
        _time_vbox = QVBoxLayout()

        _time_hbox.addWidget(self.time_txt_lb,1)
        _time_hbox.addWidget(self.time_val_lb,3)
        _latlon_hbox.addWidget(self.lat_txt_lb)
        _latlon_hbox.addWidget(self.lat_val_lb)
        _latlon_hbox.addWidget(self.long_txt_lb)
        _latlon_hbox.addWidget(self.long_val_lb)

        _time_vbox.addLayout(_time_hbox)
        _time_vbox.addLayout(_latlon_hbox)

        self.setLayout(_time_vbox)

        # txt 정렬
        self.time_txt_lb.setAlignment(Qt.AlignCenter)
        self.lat_txt_lb.setAlignment(Qt.AlignCenter)
        self.long_txt_lb.setAlignment(Qt.AlignCenter)

        self.time_txt_lb.setFont(TXT_FONT)
        self.time_val_lb.setFont(VAL_FONT)
        self.lat_txt_lb.setFont(TXT_FONT)
        self.lat_val_lb.setFont(VAL_FONT)
        self.long_txt_lb.setFont(TXT_FONT)
        self.long_val_lb.setFont(VAL_FONT)

        self.setMaximumHeight(100)

        # GPS 위젯 설정
        self.setAttribute(Qt.WA_StyledBackground, True)

        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())