# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject, pyqtSlot, QSemaphore

from viewmodel import dataVM, gpsVM, graphVM, logVM, videoVM, dataSearchVM
from packages.utils.generate_txt import TestTxt
from packages.utils.generate_data import Testdata
from packages.utils.timer import Timer
from packages.utils.video import Video
from packages.utils.enum import IOType
from view.mainView import MainView

from config import win_conf, font_conf

class MainVM(QObject):
    def __init__(self, view: MainView, model):
        super().__init__()
        self.main_view = view
        self._model = model
        sem = QSemaphore(14) # Semaphore

        # TODO: 상수 외부선언
        # 상수 및 변수 선언
        self.info_btn_name = ""
        self._data = 0
        self.now_time = ""
        self.cache_text = ""
        self.CACHE_SIZE = 100

        # 뷰모델 선언
        self.data_vm = dataVM.DataVM(self.main_view.data_view)
        self.gps_vm = gpsVM.GpsVM(self.main_view.gps_view,self._model.d.latlon_buf, sem)
        self.graph_vm = graphVM.GraphVM(self.main_view.graph_view)
        self.log_vm = logVM.LogVM(self.main_view.log_view)
        self.video_vm = videoVM.VideoVM(self.main_view.video_view)
        self.data_search_vm = dataSearchVM.DataSearchVM(self.main_view.data_search_view)

        # 스레드 선언
        self._log_th = TestTxt(self._model.d, sem)                                  # 로그
        self._temp_th = Testdata(IOType.TEMPATURE, self._model.d.temp_buf, sem)     # 온도
        self._humid_th = Testdata(IOType.HUMID, self._model.d.humi_buf, sem)        # 습도
        self._illu_th = Testdata(IOType.ILLUM, self._model.d.lux_buf, sem)          # 조도
        self._accel_th = Testdata(IOType.ACCEL, self._model.d.acc_z_buf, sem)       # 가속도
        self._pothole_th = Testdata(IOType.POTHOLE, self._model.d.pth_buf, sem)     # 포트홀
        
        self._font_video_th = Video(self._model.d.det_buf, sem)                     # 전방 비디오
        self._back_video_th = Video(self._model.d.det_buf, sem)                     # 후방 비디오 (사용 X?)
        self._time_th = Timer()                                                     # 시간

        # 스레드 전달
        self.data_vm.setThread(self._temp_th, IOType.TEMPATURE)
        self.data_vm.setThread(self._humid_th, IOType.HUMID)
        self.data_vm.setThread(self._illu_th, IOType.ILLUM)
        self.data_vm.setThread(self._accel_th, IOType.ACCEL)
        self.data_vm.setThread(self._pothole_th, IOType.POTHOLE)

        self.graph_vm.setThread(self._temp_th, IOType.TEMPATURE)
        self.graph_vm.setThread(self._humid_th, IOType.HUMID)
        self.graph_vm.setThread(self._illu_th, IOType.ILLUM)
        self.graph_vm.setThread(self._accel_th, IOType.ACCEL)
        self.graph_vm.setThread(self._pothole_th, IOType.POTHOLE)

        self.video_vm.setFrontVideoThread(self._font_video_th)
        self.video_vm.setBackVideoThread(self._back_video_th)

        # 슬롯 연결
        self._time_th.signal.connect(self._getTime)
        self._log_th.signal.connect(self._getLog)

        # 스레드 시작
        self._time_th.start()
        self._log_th.start()

        # signal 가져오기
        self.data_vm.signal.connect(self._getInfoBtnNameAndActiveState)
        self.main_view.signal.connect(self._changeFontSizeByWindSize)

    @pyqtSlot(int, int)
    def _changeFontSizeByWindSize(self, win_width: int, win_height: int) -> None:
        """
        윈도우 크기에 따른 폰트 크기 변화 메소드
        params: win_width(int) - 윈도우 폭
                win_height(int) - 윈도우 높이
        return: None
        """
        # 크기가 가장 큰 윈도우의 크기 조건
        if win_width >= win_conf["main_view"]["wide_width"] and win_height >= win_conf["main_view"]["wide_height"]:
            font_size = font_conf["size"]["huge"]
            self.video_vm.resizeFont(font_size)
            self.gps_vm.resizeFont(font_size)
            self.data_vm.resizeFont(font_size, 10, 5)
            self.log_vm.resizeFont(font_size)
            self.graph_vm.resizeFont(font_size)
            self.data_search_vm.resizeFont(font_size)
        # 크기가 중간인 윈도우의 크기 조건
        elif win_width >= win_conf["main_view"]["mid_width"] and win_height >= win_conf["main_view"]["mid_height"]:
            font_size = font_conf["size"]["big"]
            self.video_vm.resizeFont(font_size)
            self.gps_vm.resizeFont(font_size)
            self.data_vm.resizeFont(font_size, 5, 3)
            self.log_vm.resizeFont(font_size)
            self.graph_vm.resizeFont(font_size)
            self.data_search_vm.resizeFont(font_size)
        # 크기가 중간 크기이면서 작은 윈도우의 크기 조건
        elif win_width >= win_conf["main_view"]["little_wide_width"] and win_height >= win_conf["main_view"]["little_wide_height"]:
            font_size = font_conf["size"]["tall"]
            self.video_vm.resizeFont(font_size)
            self.gps_vm.resizeFont(font_size)
            self.data_vm.resizeFont(font_size, 3, 2)
            self.log_vm.resizeFont(font_size)
            self.graph_vm.resizeFont(font_size)
            self.data_search_vm.resizeFont(font_size)
        # 그 외의 윈도우 크기 조건
        else:
            font_size = font_conf["size"]["small"]
            self.video_vm.resizeFont(font_size)
            self.gps_vm.resizeFont(font_size)
            self.data_vm.resizeFont(font_size, 1, 2)
            self.log_vm.resizeFont(font_size)
            self.graph_vm.resizeFont(font_size)
            self.data_search_vm.resizeFont(font_size)


    @pyqtSlot(str, str)
    def _getLog(self, log_type: str, msg: str) -> None:
        """
        log를 얻는 pyqtslot
        @params: log_type(str) - log 수준
                msg(str) - log 메시지
        @return: None
        """
        log_msg = f"{self.now_time} : {msg}"
        # 로그메시지 전달
        self.log_vm.displayLog(log_type, log_msg)

    @pyqtSlot(str, str)
    def _getTime(self, current_day: str, current_time: str) -> None:
        """
        시간을 얻는 pyqtslot
        @params: current_day(str) - 현재 날짜
                current_time(str) - 현재 시간
        @return: None
        """
        # 현재시간 전달
        self.gps_vm.time_and_pos_vm.displayTime(current_day, current_time)
        # 현재시간 저장
        self.now_time = current_day+current_time

    @pyqtSlot(str, bool)
    def _getInfoBtnNameAndActiveState(self, info_btn_name: str, active_state: bool) -> None:
        """
        Info 버튼 이름과 활성화 상태를 가져오는 pyqtslot
        @params: info_btn_name(str) - info 버튼 이름
                    active_state(bool) - 활성화 상태
        @return: None
        """
        self.graph_vm.changeActiveIO(info_btn_name, active_state)

    def threadQuit(self) -> None:
        """
        쓰레드 종료
        @params: None
        @return: None
        """
        self.data_vm.setThread(None, IOType.TEMPATURE)
        self.data_vm.setThread(None, IOType.HUMID)
        self.data_vm.setThread(None, IOType.ILLUM)
        self.data_vm.setThread(None, IOType.ACCEL)
        self.data_vm.setThread(None, IOType.POTHOLE)

        self.graph_vm.setThread(None, IOType.TEMPATURE)
        self.graph_vm.setThread(None, IOType.HUMID)
        self.graph_vm.setThread(None, IOType.ILLUM)
        self.graph_vm.setThread(None, IOType.ACCEL)
        self.graph_vm.setThread(None, IOType.POTHOLE)

        self.video_vm.setFrontVideoThread(None)
        self.video_vm.setBackVideoThread(None)

        self._time_th.quitThread()
        self._log_th.quitThread()
        self._temp_th.quitThread()
        self._humid_th.quitThread()
        self._illu_th.quitThread()
        self._accel_th.quitThread()
        self._pothole_th.quitThread()
        self._font_video_th.quitThread()
        self._back_video_th.quitThread()
