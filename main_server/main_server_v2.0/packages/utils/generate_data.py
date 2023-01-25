from dataclasses import dataclass
import logging
from PyQt5.QtCore import QThread, pyqtSignal
import time
import random
from packages.utils.enum import IOType

class Testdata(QThread):
    signal = pyqtSignal(float, IOType)

    def __init__(self, io_type, data, sem):
        super().__init__()
        self._keep_running = True
        self._selected_graph = False
        self.io_type = io_type
        self._data = data
        self._sem = sem

    def run(self) -> None:
        """
        스테드 run
        @params: None
        @return: None
        """
        self._keep_running = True

        while self._keep_running:
            #print(f"generate_data : iotype :{self.io_type}")
            # data를 외부에 전달
            self._sem.acquire()
            self.signal.emit(float(self._data[0]), self.io_type)
            if self._selected_graph:
                self._data_q.put(float(self._data[0]))
            self._sem.release()
            time.sleep(0.1) if self.io_type == IOType.ACCEL else time.sleep(0.5)
            
    def stop(self) -> None:
        """
        스레드 중지
        @params: None
        @return: None
        """
        self._keep_running = False

    def selectGraph(self) -> None:
        """
        해당 클래스의 run 메소드를 통해 도출되는 데이터를 그래프를 그리는 곳에 사용하겠다고 선언하는 메소드
        @params: None
        @return: None
        """
        self._selected_graph = True

    def cancelGraph(self) -> None:
        """
        해당 클래스의 run 메소드를 통해 도출되는 데이터를 그래프를 그리는 곳에 사용하지 않겠다고 선언하는 메소드
        @params: None
        @return: None
        """
        self._selected_graph = False

    def quitThread(self) -> None:
        """
        쓰레드 종료
        @params: None
        @return: None
        """
        self.quit()
