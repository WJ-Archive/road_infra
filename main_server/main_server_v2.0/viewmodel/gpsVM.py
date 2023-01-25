# -*- coding: utf-8 -*-
import os
import logging

from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWebChannel import QWebChannel

from viewmodel.timeAndPosVM import TimeAndPosVM
from view.gpsView import GpsView
from packages.utils.position_test import CallHandler, TestPosdata



class GpsVM(QObject):
    def __init__(self, view: GpsView, model, sem): #model : latlon 
        super().__init__()
        self._model = model
        self._sem = sem

        # view 연결
        self.gps_view = view
        self.time_and_pos_vm = TimeAndPosVM(self.gps_view.time_pos_view)

        # GPS map(JS)과 pyqt의 데이터 연결
        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject('handler', self.handler)
        self.gps_view.map_view.page().setWebChannel(self.channel)

        # 위도, 경도 임의 테스트(쓰레드연결)
        self.position_test = TestPosdata(self._model, self._sem)
        self.position_test.signal.connect(self.handler.receive_data)
        self.position_test.signal.connect(self.time_and_pos_vm.displayLat_lon)
        self.position_test.start()

        # GPS map html 경로 전달
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/gpsmap/map.html"))
        local_url = QUrl.fromLocalFile(file_path)

        self.gps_view.map_view.load(local_url)

    def resizeFont(self, font_size: int) -> None:
        """
        video view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
        return: None
        """

        assert type(font_size) is int, logging.error("인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int:
            logging.error("font_size가 int 타입이 아닙니다.")
            return

        self.time_and_pos_vm.resizeFont(font_size)

    
