# -*- coding: utf-8 -*-
import logging
import pyqtgraph as pg

from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.Qt import QThread

from packages.utils.enum import IOType
from view.graphView import GraphView
from config import info_btn

from collections import deque

class GraphVM(QObject):
    def __init__(self, view: GraphView):
        super().__init__()
        self.graph_view = view
        self._model = None

        # 상수 및 변수 선언
        self._TIME_LIMIT = 100
        self._cnt = 0
        #self._x = []
        #self._y = []
        self.que_len = 100
        #self._x = deque(maxlen=self.que_len)
        #self._y = deque(maxlen=self.que_len)
        self._x = deque([i for i in range(0, 100)],maxlen=self.que_len)
        self._y = deque([0 for i in range(0, 100)],maxlen=self.que_len)

        self._graph_active_type = None
        self.info_btn_type_list = info_btn

        # 버튼 활성화 딕셔러니
        self._active_IObtn_dict = {IOtype: False for IOtype in IOType}

        # 그래프 그리는 행동을 제어하는 스위치 딕셔너리 선언
        self._stop_draw_IOdict = {IOtype: True for IOtype in IOType}

        # 쓰레드 딕셔너리 선언
        self._thread_IOdict = {IOtype: None for IOtype in IOType}

        self.graph_view.cbox.currentTextChanged.connect(self._selectIO)

    def _selectIO(self):
        curren_txt = self.graph_view.cbox.currentText()
        self.clickViewChange(curren_txt)


    def resizeFont(self, font_size: int) -> None:
        """
        graph view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
        return: None
        """
        assert type(font_size) is int, logging.error("인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int:
            logging.error("인자가 int 타입이 아닙니다.")
            return

        # 폰트 설정
        font = self.graph_view.graph.property("font")
        font.setPointSize(font_size)

        # view에 있는 폰트 변환 적용
        self.graph_view.graph.setFont(font)


    def setThread(self, thread: QThread, io_type: IOType) -> None:
        """
        Thread setter
        @params: thread(QThread) - 쓰레드
                io_type(IOType) - IO 타입 (enum)
        @return: None
        """

        self._thread_IOdict[io_type] = thread
        if self._thread_IOdict[io_type] is not None:
            self._thread_IOdict[io_type].signal.connect(self._drawGraph)


    @pyqtSlot(float, IOType)
    def _drawGraph(self, data: float, io_type: IOType) -> None:
        """
        데이터를 그래프에 그리는 pyqtslot
        @params: data(float) - 데이터
                io_type(IOType) - I/O 타입 (enum)
        @return: None
        """
        assert type(data) is float, logging.error("_drawGraph 메소드의 data 인자 타입오류")
        assert type(io_type) is IOType, logging.error("_drawGraph 메소드의 io_type 인자 타입오류")

        # 타입검사
        if type(data) is not float:
            logging.error("_drawGraph 메소드의 data 인자 타입오류")
            return

        if type(io_type) is not IOType:
            logging.error("_drawGraph 메소드의 io_type 인자 타입오류")
            return

        # plot
        if self._stop_draw_IOdict[io_type]:
            return
        if io_type == IOType.TEMPATURE:
            self.graph_view.graph.setTitle(self.info_btn_type_list[0])
            self.graph_view.graph.setLabel("left", "℃")
        elif io_type == IOType.HUMID:
            self.graph_view.graph.setTitle(self.info_btn_type_list[1])
            self.graph_view.graph.setLabel("left", "%")
        elif io_type == IOType.ILLUM:
            self.graph_view.graph.setTitle(self.info_btn_type_list[2])
            self.graph_view.graph.setLabel("left", "lux")
        elif io_type == IOType.ACCEL:
            self.graph_view.graph.setTitle(self.info_btn_type_list[3])
            self.graph_view.graph.setLabel("left", "g")
        else:
            self.graph_view.graph.setTitle(self.info_btn_type_list[4])
            self.graph_view.graph.setLabel("left", "개")

        self.graph_view.graph.clear()
        
        #그래프 그리는 방식 1
        """if self._cnt > self._TIME_LIMIT:
            self._cnt = 0
            self._x = []
            self._y = []

        self._cnt += 1
        self._x.append(self._cnt)
        self._y.append(data)
        self.graph_view.graph.plot(x=self._x, y=self._y, pen=pg.mkPen(width=2, color='r'))"""
        
        #그래프 그리는 방식 2
        """if self._cnt > self._TIME_LIMIT:
            self._cnt = 0
            self._x = deque(maxlen=self.que_len)
            self._y = deque(maxlen=self.que_len)
        
        self._cnt += 1
        self._x.append(self._cnt)
        self._y.append(data)
        self.graph_view.graph.plot(x=self._x, y=self._y, pen=pg.mkPen(width=2, color='b'))
        """
        
        #그래프 그리는 방식 3
        if self._cnt > self._TIME_LIMIT:
            self._y = deque([0 for i in range(0,100)], maxlen=self.que_len)
        
        self._y.append(data)
        self.graph_view.graph.plot(x=self._x, y=self._y, pen=pg.mkPen(width=2, color='b'))


    def changeActiveIO(self, info_btn_name: str, active_state: bool) -> None:
        """
        info 버튼 활성화 변환 메소드
        @params: info_btn_name(str) - info 버튼 이름
                activate_state(bool) - 활성화 상태
        @return: None
        """
        assert type(info_btn_name) is str, logging.error(f"changeActiveIO 메소드의 인자 info_btn_name이 string 타입이 아닙니다.")
        assert info_btn_name in self.info_btn_type_list, logging.error(f"changeActiveIO 메소드의 인자 info_btn_name이 리스트에 없습니다.")
        assert type(active_state) is bool, logging.error(f"changeActiveIO 메소드의 인자 active_state가 bool 타입이 아닙니다.")

        # 타입검사
        if type(info_btn_name) is not str:
            logging.error(f"changeActiveIO 메소드의 인자 info_btn_name이 string 타입이 아닙니다.")
            return
        elif not(info_btn_name in self.info_btn_type_list):
            logging.error(f"changeActiveIO 메소드의 인자 info_btn_name이 리스트에 없습니다.")
            return
        if type(active_state) is not bool:
            logging.error(f"changeActiveIO 메소드의 인자 active_state가 bool 타입이 아닙니다.")
            return

        # data 버튼 "온도"가 눌렸을 때 상태 변화
        if info_btn_name == self.info_btn_type_list[0]:
            self._changeComboBoxItemAndActiveIOState(self.info_btn_type_list[0], IOType.TEMPATURE, active_state)

        # data 버튼 "습도"가 눌렸을 때 상태 변화
        elif info_btn_name == self.info_btn_type_list[1]:
            self._changeComboBoxItemAndActiveIOState(self.info_btn_type_list[1], IOType.HUMID, active_state)

        # data 버튼 "조도"가 눌렸을 때 상태 변화
        elif info_btn_name == self.info_btn_type_list[2]:
            self._changeComboBoxItemAndActiveIOState(self.info_btn_type_list[2], IOType.ILLUM, active_state)

        # data 버튼 "가속도"가 눌렸을 때 상태 변화
        elif info_btn_name == self.info_btn_type_list[3]:
            self._changeComboBoxItemAndActiveIOState(self.info_btn_type_list[3], IOType.ACCEL, active_state)

        # data 버튼 "포트홀"이 눌렸을 때 상태 변화
        elif info_btn_name == self.info_btn_type_list[4]:
            self._changeComboBoxItemAndActiveIOState(self.info_btn_type_list[4], IOType.POTHOLE, active_state)

        else:
            logging.error("changeActiveIO 메소드 오류")
            return


    def clickViewChange(self, info_btn_name: str) -> None:
        """
        그래프 뷰 내용을 바꾸는 메소드
        @params: info_btn_name(str)
        @return: None
        """
        assert type(info_btn_name) is str, logging.error("clickViewChange 메소드의 info_btn_name 인자 타입오류")
        
        # 타입검사
        if type(info_btn_name) is not str:
            logging.error("clickViewChange 메소드의 info_btn_name 인자 타입오류")
            return
        
        if info_btn_name == self.info_btn_type_list[0]:
            self._changeDrawingState(IOType.TEMPATURE)

        elif info_btn_name == self.info_btn_type_list[1]:
            self._changeDrawingState(IOType.HUMID)

        elif info_btn_name == self.info_btn_type_list[2]:
            self._changeDrawingState(IOType.ILLUM)

        elif info_btn_name == self.info_btn_type_list[3]:
            self._changeDrawingState(IOType.ACCEL)

        elif info_btn_name == self.info_btn_type_list[4]:
            self._changeDrawingState(IOType.POTHOLE)

        else:
            self._graph_active_type = None
            self._resetAxisContents()
            return

    def _resetAxisContents(self) -> None:
        """
        x 축과 y축의 내용을 모두 없애주는 메소드
        @params: None
        @return: None
        """
        #self._x = []
        #self._y = []
        #self._x = deque(maxlen=self.que_len)
        #self._y = deque(maxlen=self.que_len)
        self._y = deque([0 for i in range(0,100)], maxlen=self.que_len)



    def _changeDrawingState(self, io_type: IOType) -> None:
        """
        그리는 상태를 변화하는 메소드
        @params: io_type(IOType) - I/O 타입 (enum)
        @return: None
        """
        assert type(io_type) is IOType, logging.error(f"_changeDrawingState 메소드의 io_type 인자가 IOType이 아닙니다.")

        # 타입검사
        if type(io_type) is not IOType:
            logging.error(f"_changeDrawingState 메소드의 io_type 인자가 IOType이 아닙니다.")
            return

        if not(io_type in IOType):
            logging.error(f"_changeDrawingState 메소드의 io_type 인자가 IOType에 정의되어 있지 않습니다.")
            return

        if not self._thread_IOdict[io_type].isRunning():
            self._active_IObtn_dict[io_type] = False
            # self._stop_draw_IOdict = {key: True for key, _ in self._stop_draw_IOdict.items()}
            self._stop_draw_IOdict[io_type] = True
            return

        if self._graph_active_type != io_type:
            self._graph_active_type = io_type
            self._resetAxisContents()
            for k, v in self._stop_draw_IOdict.items():
                if k == io_type:
                    continue
                self._stop_draw_IOdict[k] = True
            self._active_IObtn_dict[io_type] = False

        if self._active_IObtn_dict[io_type]:
            self._active_IObtn_dict[io_type] = False
            self._stop_draw_IOdict[io_type] = True
        else:
            self._active_IObtn_dict[io_type] = True
            self._stop_draw_IOdict[io_type] = False

    def _changeComboBoxItemAndActiveIOState(self, item_name: str, io_type: IOType, active_state: bool) -> None:
        """
        Graphic view의 콤보박스 상태 변화 및 IO 상태 변화 메소드
        @params: item_name(str) - 콤보박스에 추가할 아이템 이름
                io_type(IOType) - I/O 타입(enum)
                active_state(bool) - 버튼 활성화 상태
        @return: None
        """
        assert type(item_name) is str, logging.error("_changeComboBoxItemAndActiveIOState 메소드의 item_name 인자 타입 에러")
        assert type(io_type) is IOType, logging.error("_changeComboBoxItemAndActiveIOState 메소드의 io_type 인자 타입 에러")
        assert type(active_state) is bool, logging.error("_changeComboBoxItemAndActiveIOState 메소드의 active_state 인자 타입 에러")

        # 타입 검사
        if type(item_name) is not str:
            logging.error("_changeComboBoxItemAndActiveIOState 메소드의 item_name 인자 타입 에러")
            return

        if type(io_type) is not IOType:
            logging.error("_changeComboBoxItemAndActiveIOState 메소드의 io_type 인자 타입 에러")
            return

        if not(io_type in IOType):
            logging.error(f"_changeDrawingState 메소드의 io_type 인자가 IOType에 정의되어 있지 않습니다.")
            return
        
        if type(active_state) is not bool:
            logging.error("_changeComboBoxItemAndActiveIOState 메소드의 active_state 인자 타입 에러")
            return

        self._active_IObtn_dict[io_type] = active_state
        if active_state:
            self.graph_view.cbox.addItem(item_name)
            self.graph_view.cbox.model().sort(Qt.AscendingOrder)
        else:
            self._stop_draw_IOdict[io_type] = True
            idx = self.graph_view.cbox.findText(item_name)
            if idx == self.graph_view.cbox.currentIndex():
                self.graph_view.cbox.setCurrentIndex(0)
            self.graph_view.cbox.removeItem(idx)