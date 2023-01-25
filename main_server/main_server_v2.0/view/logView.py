# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextBrowser, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from config import win_conf, font_conf


class LogView(QWidget):
    def __init__(self, stylesheet="qss/logWin.qss"):
        super().__init__()

        # 폰트 설정 정의
        FRONT_TYPE = font_conf["type"]["Arial"]
        FRONT_SIZE = font_conf["size"]["small"]
        FONT = QFont(FRONT_TYPE, FRONT_SIZE)

        # 레이블 생성 및 설정
        self.log_status_lb = QWidget(objectName="log_status_lb")
        grid_layout = QGridLayout()

        """
        self.info_txt = QLabel("[정보]")
        self.info_txt.setFont(FONT)
        self.info_txt.setAlignment(Qt.AlignCenter)

        self.info_val = QLabel("0")
        self.info_val.setFont(FONT)
        self.info_val.setAlignment(Qt.AlignLeft)
        """
        self.warn_txt = QLabel("[경고]", objectName="warn_txt")
        self.warn_txt.setFont(FONT)
        self.warn_txt.setAlignment(Qt.AlignCenter)

        self.warn_val = QLabel("0", objectName="warn_val")
        self.warn_val.setFont(FONT)
        self.warn_val.setAlignment(Qt.AlignLeft)

        self.err_txt = QLabel("[오류]", objectName="err_txt")
        self.err_txt.setFont(FONT)
        self.err_txt.setAlignment(Qt.AlignCenter)

        self.err_val = QLabel("0", objectName="err_val")
        self.err_val.setFont(FONT)
        self.err_val.setAlignment(Qt.AlignLeft)

        ######## 추가 ########
        """self.det_txt = QLabel("[탐지]", objectName="det_txt")
        self.det_txt.setFont(FONT)
        self.det_txt.setAlignment(Qt.AlignCenter)

        self.det_val = QLabel("0", objectName="det_val")
        self.det_val.setFont(FONT)
        self.det_val.setAlignment(Qt.AlignLeft)"""
        ######################
        self.txt_brw = QTextBrowser(objectName="txt_brw")
        self.txt_brw.setFont(FONT)

        # 위젯 배치
        """
        grid_layout.addWidget(self.info_txt, 0, 0)
        grid_layout.addWidget(self.info_val, 0, 1)
        """
        grid_layout.addWidget(self.warn_txt, 0, 2)
        grid_layout.addWidget(self.warn_val, 0, 3)
        grid_layout.addWidget(self.err_txt, 0, 4)
        grid_layout.addWidget(self.err_val, 0, 5)
        #grid_layout.addWidget(self.det_txt, 0, 6) #추가
        #grid_layout.addWidget(self.det_val, 0, 7) #추가

        self.log_status_lb.setLayout(grid_layout)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.log_status_lb)
        self.vbox.addWidget(self.txt_brw)
        self.setLayout(self.vbox)

        # 위젯 크기 및 그 외 설정
        self.setAttribute(Qt.WA_StyledBackground, True)

        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())