# -*- coding: utf-8 -*-
import numpy
from PyQt5.QtCore import QThread, pyqtSignal
from model.det import front_frame

"""
수정:
프레임 저장 하는 쓰레드를 생성하여 버퍼에서 따로 스트리밍 시켰었는데 객체 정보는 UDP소켓으로 전송하고 프레임은 TCP소켓으로 스트리밍 하여서
속도 문제가 발생하여 프레임 저장시 타이밍이 안맞음. 따라서 프레임을 버퍼에 저장하지 않고 Video.py 에서는 스트리밍 만 하고 model로 det_buf를 넘겨준뒤
객체정보가 UDP를 통해 날아오면 해당 프레임 저장하도록 변경
"""

class Video(QThread):
    signal = pyqtSignal(bool, numpy.ndarray)

    def __init__(self, model, sem):
        super().__init__()
        self._capture = None
        self._WIDTH = 640
        self._HEIGHT = 480
        self._keep_running = True
        self._model = model # 추가 (프레임)
        self._sem = sem #추가 (세마포어)
        

    def connectVideo(self):
        try:
            self.f = front_frame.Frame()
            #yolo v5 모델과 tracker 모델 로드 하는 속도가 있어서 ConnectVideo가 너무 느려지는 이슈가 있음. init 에 넣으면 TCP 소켓 연결될때까지 프로그램 실행 안됨
        except Exception as e:
            print(e)

    def abortVideo(self):
        self._keep_running = False

    def resumeVideo(self):
        self._keep_running = True

    def disconnectVideo(self):
        ...
        #self._capture.release()

    def run(self) -> None:
        """
        쓰레드 시작
        @params: None
        @return: None
        """   
        self.connectVideo() # 전방카메라 Toggle시 연결 시작
        while True:
            self._sem.acquire()
            det = []
            if self._keep_running:
                frame = self.f.get_frame()
                if frame is not None:
                    if(len(self._model)):
                        det = self._model.pop()
                        print(det)
                    ret = True if len(det) else False
                    self.signal.emit(ret, frame)
                
            self._sem.release()


    def quitThread(self) -> None:
        """
        쓰레드 종료
        @params: None
        @return: None
        """
        if self._capture is not None:
            self._capture.release()
        self.quit()
