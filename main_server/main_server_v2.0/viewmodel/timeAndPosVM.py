# -*- coding: utf-8 -*-
import logging
from PyQt5.QtCore import QObject
from view.timeAndPosView import TimeAndPosView

class TimeAndPosVM(QObject):
    def __init__(self, view: TimeAndPosView):
        super().__init__()
        self.time_and_pos_view = view
        

    def displayLat_lon(self, latlon : list) -> None: # 추가
        #추가(latitude, longtiude)
        """
        좌표 표시 메소드 ()
        """
        
        self.time_and_pos_view.lat_val_lb.display(latlon[0])
        self.time_and_pos_view.long_val_lb.display(latlon[1])

    def displayTime(self, current_day: str, current_time: str) -> None:
        """
        시간 표시 메소드
        @params: current_day(str) - 현재 날짜
                current_time(str) - 현재 시간
        @return: None
        """
        
        self.time_and_pos_view.time_val_lb.display(current_day+" "+current_time)

    def resizeFont(self, font_size: int) -> None:
        """
        time and position view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
        return: None
        """
        assert type(font_size) is int, logging.error("인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int:
            logging.error("font_size가 int 타입이 아닙니다.")
            return

        # 폰트 설정
        font = self.time_and_pos_view.time_txt_lb.property("font")
        font.setPointSize(font_size)

        # view에 있는 폰트 변환 적용
        self.time_and_pos_view.time_txt_lb.setFont(font)
        self.time_and_pos_view.time_val_lb.setFont(font)
        self.time_and_pos_view.lat_txt_lb.setFont(font)
        self.time_and_pos_view.lat_val_lb.setFont(font)
        self.time_and_pos_view.long_txt_lb.setFont(font)
        self.time_and_pos_view.long_val_lb.setFont(font)
