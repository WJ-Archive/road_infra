# -*- coding: utf-8 -*-
from PyQt5.QtCore import (QTimer, QThread, pyqtSignal, QDateTime)


class Timer(QThread):
    signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        # 타이머 생성 및 설정
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.run)

        self._timer.start()

    def run(self) -> None:
        """
        쓰레드 시작
        @params: None
        @return: None
        """
        # 현재시간 포멧 설정
        current_day = QDateTime.currentDateTime().toString("yyyy.MM.dd.")
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")

        # 현재시간 emit
        self.signal.emit(current_day, current_time)

    def quitThread(self) -> None:
        """
        쓰레드 종료
        @params: None
        @return: None
        """
        self.quit()