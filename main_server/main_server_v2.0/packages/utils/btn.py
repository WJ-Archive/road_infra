# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from config import font_conf, info_btn
from packages.utils.enum import IOType


class InfoBtn(QWidget):
    """
    기온, 습도, 조도, 가속도, 포트홀 유무 정보가 담긴 버튼 클래스
    """
    signal = pyqtSignal(IOType)

    def __init__(self, info_name: str):
        super(QWidget, self).__init__()

        assert type(info_name) is str, logging.error("InfoBtn 생성자의 info_name 인자가 string이 아닙니다.")

        if type(info_name) is not str:
            logging.error("InfoBtn 생성자의 info_name 인자가 string이 아닙니다.")
            return

        FONT_SIZE = font_conf["size"]["small"]
        FONT_TYPE = font_conf["type"]["Arial"]
        FONT = QFont(FONT_TYPE, FONT_SIZE)
        self.name = info_name

        # layout 설정
        _vbox = QVBoxLayout()
        _hbox = QHBoxLayout()

        # label 및 버튼 생성
        self.info_name_lb = QLabel(self, objectName="info_name_lb")
        self.info_val_lb = QLabel(self, objectName="info_val_lb")
        self.unit_lb = QLabel(self, objectName="unit_lb")

        # 텍스트 입력
        self.info_name_lb.setText(info_name)
        self.info_val_lb.setText("")
        self.unit_lb.setText("")

        # 폰트 설정
        self.info_name_lb.setFont(FONT)
        self.info_val_lb.setFont(FONT)
        self.unit_lb.setFont(FONT)

        # label의 텍스트 위치 설정
        self.info_name_lb.setAlignment(Qt.AlignCenter)
        self.info_val_lb.setAlignment(Qt.AlignRight)
        self.unit_lb.setAlignment(Qt.AlignLeft)
        self.unit_lb.setAlignment(Qt.AlignVCenter)

        # 위젯 배경색 변경
        self.setAttribute(Qt.WA_StyledBackground, True)

        # 레이아웃에 위젯 추가
        self.spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        _hbox.addItem(self.spacer1)
        _hbox.addWidget(self.info_val_lb)
        _hbox.addWidget(self.unit_lb)
        _hbox.addItem(self.spacer1)
        _vbox.addWidget(self.info_name_lb)
        _vbox.addLayout(_hbox)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setLayout(_vbox)

    def setFont(self, txt_font: QFont, val_font: QFont, unit_font: QFont) -> None:
        """
        폰트 설정 메소드
        params: txt_font(QFont) - label 텍스트 폰트
                val_font(QFont) - label value 폰트
                unit_font(QFont) - unit 폰트
        return: None
        """
        if type(txt_font) is not QFont or type(val_font) is not QFont:
            logging.ERROR("인자가 QFont 타입이 아닙니다.")
            return

        self.info_name_lb.setFont(txt_font)
        self.info_val_lb.setFont(val_font)
        self.unit_lb.setFont(unit_font)

    def mousePressEvent(self, event) -> None:
        """
        마우스 클릭 이벤트
        @params: event
        @return: none
        """
        type = None
        name = self.findChild(QLabel, "info_name_lb").text()
        if name == info_btn[0]:
            type = IOType.TEMPATURE
        elif name == info_btn[1]:
            type = IOType.HUMID
        elif name == info_btn[2]:
            type = IOType.ILLUM
        elif name == info_btn[3]:
            type = IOType.ACCEL
        elif name == info_btn[4]:
            type = IOType.POTHOLE
        else:
            logging.error("없는 타입입니다.")
            return

        self.signal.emit(type)

    def getName(self):
        """
        이름 getter
        @params: None
        @return: None
        """
        return self.name
