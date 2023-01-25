# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# main.py 기준 절대 주소 사용
from config import win_conf, font_conf, label_conf


class VideoView(QWidget):
    """
    전방 및 후방 카메라의 화면 위젯
    """
    def __init__(self, stylesheet="qss/videoWin.qss"):
        super(QWidget, self).__init__()

        # 폰트 정의 및 설정
        FONT_SIZE = font_conf["size"]["small"]
        FONT_TYPE = font_conf["type"]["Arial"]
        FONT = QFont(FONT_TYPE, FONT_SIZE)
        FONT.setBold(True)

        # 그리드 레이아웃 생성
        _vbox_layout = QVBoxLayout()

        # 비디오 화면을 배치할 레이블 생성 및 설정
        self.front_view = QLabel(objectName="front_view")
        self.back_view = QLabel(objectName="back_view")

        self.front_view.setScaledContents(True)
        self.back_view.setScaledContents(True)
        self.front_view.setAlignment(Qt.AlignCenter)
        self.back_view.setAlignment(Qt.AlignCenter)
        self.front_view.setFont(FONT)
        self.back_view.setFont(FONT)
        self.front_view.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.back_view.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # 버튼 생성
        self.front_txt_btn = QPushButton("전방영상 OFF", objectName="front_txt_btn")
        self.back_txt_btn = QPushButton("후방영상 OFF", objectName="back_txt_btn")

        # 버튼 설정
        self.front_txt_btn.setFont(FONT)
        self.back_txt_btn.setFont(FONT)

        # 그리드 레이아웃에 배치
        _vbox_layout.addWidget(self.front_txt_btn)
        _vbox_layout.addWidget(self.front_view)
        _vbox_layout.addWidget(self.back_txt_btn)
        _vbox_layout.addWidget(self.back_view)

        self.setLayout(_vbox_layout)

        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())
            self.setAttribute(Qt.WA_StyledBackground, True)
