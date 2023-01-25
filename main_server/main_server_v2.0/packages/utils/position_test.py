from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import time
import random

class CallHandler(QObject):
    def __init__(self):
        super(CallHandler, self).__init__()
        self.data = None;

    @pyqtSlot(list)
    def receive_data(self, data):
        if self.data == None or abs(self.data[0] - data[0]) > 0.00001 or abs(self.data[1] - data[1]) > 0.00001:
            print("handler data",self.data)
            print("handler data",data)
            self.data = data


    @pyqtSlot(result=list)
    def test(self):
        return self.data # GPS 정보 전달(경도, 위도)

class TestPosdata(QThread):
    signal = pyqtSignal(list)

    def __init__(self, model, sem):
        super().__init__()
        self._keep_running = True
        self._selected_graph = False
        
        self.lat = 37.58169
        self.lon = 126.7899
        self.latlon = []
        self._model = model
        self._sem = sem

    def run(self) -> None:
        """
        스테드 run
        @params: None
        @return: None
        """
        self._keep_running = True

        while self._keep_running:
            self._sem.acquire()
            
            # TODO: 통합시 수정요망
            """if random.uniform(0, 1) > 0.5:
                self.lat = self.lat + random.uniform(0, 1)/1000
            else:
                self.lat = self.lat - random.uniform(0, 1) / 1000

            if random.uniform(0, 1) > 0.5:
                self.lon = self.lon + random.uniform(0, 1)/1000
            else:
                self.lon = self.lon - random.uniform(0, 1) / 1000
            """
            if(len(self._model)):
                self.latlon = [float(self._model[0]), float(self._model[1])]
                self.signal.emit(self.latlon)
            self._sem.release()

            time.sleep(0.5)


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
