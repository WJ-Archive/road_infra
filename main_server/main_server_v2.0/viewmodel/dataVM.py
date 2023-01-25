# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.Qt import QThread

from view.dataView import DataView
from packages.utils.enum import IOType

class DataVM(QObject):

    signal = pyqtSignal(str, bool)

    def __init__(self, view: DataView):
        super().__init__()
        self.data_view = view
        self._model = None
        self.qss_path = "qss/dataWin.qss"

        # 버튼 활성화 변수를 위한 딕셔너리 선언
        self.active_io_btn_dict = {key: False for key in IOType}

        # 쓰레드 딕셔너리 선언
        self._thread_IOtype_dict = {key: None for key in IOType}
        #{<IOType.TEMPATURE: 1>: None, <IOType.HUMID: 2>: None, <IOType.ILLUM: 3>: None, <IOType.ACCEL: 4>: None, <IOType.POTHOLE: 5>: None}

        # data_view 버튼 개체가 담긴 딕셔너리 선언
        self._data_view_btn_dict = {
            IOType.TEMPATURE: self.data_view.temp_info_btn,
            IOType.HUMID: self.data_view.humid_info_btn,
            IOType.ILLUM: self.data_view.illum_info_btn,
            IOType.ACCEL: self.data_view.acc_info_btn,
            IOType.POTHOLE: self.data_view.pothole_info_btn,
        }

        # 버튼 클릭 이벤트
        self.data_view.temp_info_btn.signal.connect(self._toggleIOBtn)
        self.data_view.humid_info_btn.signal.connect(self._toggleIOBtn)
        self.data_view.illum_info_btn.signal.connect(self._toggleIOBtn)
        self.data_view.acc_info_btn.signal.connect(self._toggleIOBtn)
        self.data_view.pothole_info_btn.signal.connect(self._toggleIOBtn)


    def resizeFont(self, font_size: int, big_size: int = 0, small_size: int =0) -> None:
        """
        data view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
                big_size(int) - font_size + big_size 값의 글자 크기
                small_size(int) - font_size - small_size 값의 글자 크기
        return: None
        """
        assert type(font_size) is int, logging.error("font_size인자가 int 타입이 아닙니다.")
        assert type(big_size) is int, logging.error("big_size인자가 int 타입이 아닙니다.")
        assert type(small_size) is int, logging.error("small_size인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int or type(big_size) is not int or type(small_size) is not int:
            logging.error("인자가 int 타입이 아닙니다.")
            return

        # 폰트 설정
        txt_font = self.data_view.temp_info_btn.info_name_lb.property("font")
        txt_font.setPointSize(font_size)

        val_font = self.data_view.temp_info_btn.info_val_lb.property("font")
        val_font.setPointSize(font_size + big_size)

        unit_font = self.data_view.temp_info_btn.unit_lb.property("font")
        unit_font.setPointSize(font_size - small_size)

        # view에 있는 폰트 변환 적용
        self.data_view.temp_info_btn.setFont(txt_font, val_font, unit_font)
        self.data_view.humid_info_btn.setFont(txt_font, val_font, unit_font)
        self.data_view.illum_info_btn.setFont(txt_font, val_font, unit_font)
        self.data_view.acc_info_btn.setFont(txt_font, val_font, unit_font)
        self.data_view.pothole_info_btn.setFont(txt_font, val_font, unit_font)

    def setThread(self, thread: QThread, io_type: IOType) -> None:
        """
        쓰레드 세터
        @params: thread(QThread) - 기온 쓰레드
                io_type(IOType) - I/O 타입 (enum)
        @return: None
        """

        self._thread_IOtype_dict[io_type] = thread
        if thread is not None:
            self._thread_IOtype_dict[io_type].signal.connect(self._setDataToText) # generate_data 에서 emit로 날린 data,iotype 들어옴

    @pyqtSlot(float, IOType)
    def _setDataToText(self, data: float, io_type: IOType) -> None:
        """
        데이터를 text에 입력하는 메소드
        @params: data(float) - 입력데이터
                io_type(IOType) - I/O 타입 (enum)
        @return: None
        """
        assert type(data) is float, logging.error(f"{self._setDataToText.__name__} 메소드의 data 인자의 타입이 float이 아닙니다.")
        assert type(io_type) is IOType, logging.error(f"{self._setDataToText.__name__} 메소드의 io_type 인자의 타입이 IOType가 아닙니다.")

        if type(data) is not float:
            logging.error(f"{self._setDataToText.__name__} 메소드의 data 인자의 타입이 float이 아닙니다.")
            return

        if type(io_type) is not IOType:
            logging.error(f"{self._setDataToText.__name__} 메소드의 io_type 인자의 타입이 IOType가 아닙니다.")
            return

        if io_type == IOType.TEMPATURE:
            self.data_view.temp_info_btn.info_val_lb. \
                setText(str(round(data, 1))) #버튼에 settext
        elif io_type == IOType.HUMID:
            self.data_view.humid_info_btn.info_val_lb. \
                setText(str(round(data, 1)))
        elif io_type == IOType.ILLUM:
            self.data_view.illum_info_btn.info_val_lb. \
                setText(str(round(data, 1)))
        elif io_type == IOType.ACCEL:
            self.data_view.acc_info_btn.info_val_lb. \
                setText(str(round(data, 1)))
        elif io_type == IOType.POTHOLE:
            self.data_view.pothole_info_btn.info_val_lb. \
                setText(str(int(data)))
        else:
            return

    def _toggleIOBtn(self, io_type: IOType) -> None:
        """
        I/O 토글 버튼
        @params: io_type(IOType) - I/O 타입 (enum)
        @return: None
        """
        assert type(io_type) is IOType, logging.error(f"{self.toggleIOBtn.__name__}메소드에서 io_type인자가 IOType 타입이 아닙니다.")

        if type(io_type) is not IOType:
            logging.error(f"{self.toggleIOBtn.__name__}메소드에서 io_type인자가 IOType 타입이 아닙니다.")
            return

        # TODO: 빠르게 클릭할 경우 값이 안나오는 경우가 있음.
        if self.active_io_btn_dict[io_type] is False:
            self._thread_IOtype_dict[io_type].start()
            self._data_view_btn_dict[io_type].setProperty("toggle", "true")
            if io_type == IOType.TEMPATURE:
                self._data_view_btn_dict[io_type].unit_lb.setText("℃")
            elif io_type == IOType.HUMID:
                self._data_view_btn_dict[io_type].unit_lb.setText("%")
            elif io_type == IOType.ILLUM:
                self._data_view_btn_dict[io_type].unit_lb.setText("lux")
            elif io_type == IOType.ACCEL:
                self._data_view_btn_dict[io_type].unit_lb.setText("g")
            elif io_type == IOType.POTHOLE:
                self._data_view_btn_dict[io_type].unit_lb.setText("개")
            self.active_io_btn_dict[io_type] = True
            self._getNameAndStateOfInfoBtn(self._data_view_btn_dict[io_type].getName(), True)

        else:
            self._thread_IOtype_dict[io_type].stop()
            self._data_view_btn_dict[io_type].setProperty("toggle", "false")
            self._data_view_btn_dict[io_type].info_val_lb.setText("")
            self._data_view_btn_dict[io_type].unit_lb.setText("")
            self.active_io_btn_dict[io_type] = False
            self._getNameAndStateOfInfoBtn(self._data_view_btn_dict[io_type].getName(), False)

        self._setQss(self.qss_path, self._data_view_btn_dict[io_type])

    def _getNameAndStateOfInfoBtn(self, info_btn_name: str, active_state: bool) -> None:
        """
        Info 버튼 이름과 활성화 상태를 가져오는 pyqtslot
        @params: info_btn_name(str) - 버튼이름
                active_state(bool) - 활성화 상태
        @return: None
        """
        self.signal.emit(info_btn_name, active_state)

    def _setQss(self, qss_path: str, widget: QWidget)-> None:
        """
        qss 적용 메소드
        params: qss_path(str) - qss 파일이 있는 경로
                widget(QWidget) - 적용할 widget 개체
        return : None
        """
        with open(qss_path, "r") as file:
            widget.setStyleSheet(file.read())
