# -*- coding: utf-8 -*-



from PyQt5.QtCore import (QThread, pyqtSignal)
import time
#추가
#position_test.py 에서 DB에 있는 데이터 다 가져와서 만들줄알고, 여기선 실시간으로 찍을려고 만들었는데 position_test.py 에서 실시간으로 찍는다고해서 필요없어짐
class Position(QThread):
    signal = pyqtSignal(str, str)

    def __init__(self, model, sem):
        super().__init__()
        self._model = model #latlon
        self._sem = sem
        self._latitude = '0.0'
        self._longitude = '0.0'

    def run(self) -> None:
        """
        쓰레드 시작
        @params: None
        @return: None
        """
        while(True):
            self._sem.acquire()
            if(len(self._model)):
                self._latitude = str(self._model[0])
                self._longitude = str(self._model[1])
                #print(f"lat lon pos.py {self._latitude, self._longitude}")

            # 현재시 좌표 emit
            self.signal.emit(self._latitude, self._longitude)
            self._sem.release()
            time.sleep(0.5)

    def quitThread(self) -> None:
        """
        쓰레드 종료
        @params: None
        @return: None
        """
        self.quit()