# -*- coding: utf-8 -*-
import sys, os
import psutil
import gc, time

from config import win_conf, strings
from view.mainView import MainView
from viewmodel.mainVM import MainVM

from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QCloseEvent
from model.data_model import Data_Model

#MVVM 
#1. 센서로부터 읽어오는 데이터 버퍼에 저장 & DBMS 저장 (data_model.py , dq.py) TODO : 시간날때 ORM 이용하여 SQL 구문 객체화 할것!
#2. View(mainView.py) : 위젯 구성 & ViewModel 에서 전송된 데이터를 받아 PyQT로 시각화.
#3. ViewModel(mainVM.py) : 버퍼에 저장된 데이터 시각화 할 수 있도록 데이터 변환 및 View로 전달(emit)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.model = Data_Model()
        self.model.run()

        MIN_WIN_WIDTH = win_conf["main_view"]["min_width"]
        MIN_WIN_HEIGHT = win_conf["main_view"]["min_height"]
        DEFAULT_WIN_WIDTH = win_conf["main_view"]["default_width"]
        DEFAULT_WIN_HEIGHT = win_conf["main_view"]["default_height"]

        # 메인 윈도우 타이틀
        self.setWindowTitle(strings["window_title"])
        
        # 윈도우 사이즈 설정
        self.resize(DEFAULT_WIN_WIDTH, DEFAULT_WIN_HEIGHT)
        self.setMinimumSize(MIN_WIN_WIDTH, MIN_WIN_HEIGHT)

        # 메인 뷰 선언
        self.main_view = MainView()

        # 메인 뷰모델 선언
        self.main_vm = MainVM(self.main_view, self.model)

        # 메인 위젯 배치
        self.setCentralWidget(self.main_view)

        # 센터 배치
        self._posCenter()
        self.show()

    def _posCenter(self):
        """
        메인 윈도우 팝업 시, 메인 윈도우를 화면의 중앙에 위치하게 하는 메소드
        @params: None
        @return: None
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _threadQuit(self) -> None:
        """
        쓰레드 종료
        @params: None
        @return: None
        """
        self.main_vm.threadQuit()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        윈도우 종료 이벤트
        @params: event(QCloseEvent) - 이벤트
        @return: None
        """
        reply = QMessageBox.question(self, 'Message', strings["quit_msg"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 모든 쓰레드 종료
            self._threadQuit()
            event.accept()
            self.exit_program()
        else:
            event.ignore()
    
    def exit_program(self):
        time.sleep(1)
        process = psutil.Process(parent_process_id)
        for proc in process.children(recursive=True):
            print(f"child process {proc.pid} terminate")
            proc.kill()
        print(f"Parent process {process.pid} terminate")
        gc.collect()
        process.kill()

if __name__ == '__main__':
    parent_process_id = os.getpid()
    app = QApplication(sys.argv)
    form = MainWindow()
    sys.exit(app.exec_())
