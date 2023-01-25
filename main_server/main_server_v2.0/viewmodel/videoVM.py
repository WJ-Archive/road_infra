# -*- coding: utf-8 -*-
import cv2
import numpy
import logging
import datetime

from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage

from view.videoView import VideoView


class VideoVM(QObject):
    def __init__(self, view: VideoView):
        super().__init__()
        self.video_view = view
        self._model = None

        self._empty_front_view = True
        self._empty_back_view = True

        self._front_video_th = None
        self._back_video_th = None

        self.video_view.front_txt_btn.setCheckable(True)
        self.video_view.back_txt_btn.setCheckable(True)

        self.video_view.front_txt_btn.toggled.connect(self.toggleFrontVideoBtn)
        self.video_view.back_txt_btn.toggled.connect(self.toggleBackVideoBtn)


    def resizeFont(self, font_size: int) -> None:
        """
        video view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
        return: None
        """

        assert type(font_size) is int, logging.error("인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int:
            logging.error("인자가 int 타입이 아닙니다.")
            return

        # 폰트 설정
        txt_font = self.video_view.front_txt_btn.property("font")
        txt_font.setPointSize(font_size)

        # view에 있는 폰트 변환 적용
        self.video_view.front_txt_btn.setFont(txt_font)
        self.video_view.back_txt_btn.setFont(txt_font)
        self.video_view.front_view.setFont(txt_font)
        self.video_view.back_view.setFont(txt_font)


    @pyqtSlot(bool)
    def toggleFrontVideoBtn(self, state: bool ) -> None:
        self.video_view.front_txt_btn.setStyleSheet(
            "background-color: %s" % ({True: "#E1FA6F", False: "#9CB9F0"}[state]))

        if state is True:
            self.video_view.front_txt_btn.setText("전방영상 ON")
            self._empty_front_view = False

            if self._front_video_th.isRunning():
                self.video_view.front_view.setText("로딩중")
                self._front_video_th.resumeVideo()
                return
            else:
                self.video_view.front_view.setText("로딩중")
                self._front_video_th.start()
        else:
            self.video_view.front_txt_btn.setText("전방영상 OFF")
            self._front_video_th.abortVideo()
            self._empty_front_view = True
            self.video_view.front_view.clear()

    @pyqtSlot(bool)
    def toggleBackVideoBtn(self, state: bool) -> None:
        self.video_view.back_txt_btn.setStyleSheet(
            "background-color: %s" % ({True: "#E1FA6F", False: "#9CB9F0"}[state]))

        if state is True:
            self.video_view.back_txt_btn.setText("전방영상 ON")
            self._empty_back_view = False

            if self._back_video_th.isRunning():
                self.video_view.back_view.setText("로딩중")
                self._back_video_th.resumeVideo()
                return
            else:
                self.video_view.back_view.setText("로딩중")
                self._back_video_th.start()
        else:
            self.video_view.back_txt_btn.setText("전방영상 OFF")
            self._back_video_th.abortVideo()
            self._empty_back_view = True
            self.video_view.back_view.clear()

    @pyqtSlot(bool, numpy.ndarray)
    def inputFrontVideo(self, is_working, video):
        if(is_working):
            self.save_frame(video)
        rgbImage = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                         QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        front_video = QPixmap(convertToQtFormat)
        widget_width = self.video_view.width()
        widget_height = self.video_view.height()

        if not self._empty_front_view:
            self.video_view.front_view.setPixmap(front_video)
            #self.video_view.front_view.setPixmap(front_video.scaled(widget_width * .38, widget_height * .38))

    @pyqtSlot(bool, numpy.ndarray)
    def inputBackVideo(self, is_working, video):
        rgbImage = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                   QImage.Format_RGB888)
        convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
        back_video = QPixmap(convertToQtFormat)

        widget_width = self.video_view.width()
        widget_height = self.video_view.height()

        # print(f"width: {widget_width}, height: {widget_height}")

        if not self._empty_back_view:
            self.video_view.back_view.setPixmap(back_video.scaled(widget_width * .38, widget_height * .38))

    def setFrontVideoThread(self, thread):
        self._front_video_th = thread
        if thread is not None:
            self._front_video_th.signal.connect(self.inputFrontVideo)

    def setBackVideoThread(self, thread):
        self._back_video_th = thread
        if thread is not None:
            self._back_video_th.signal.connect(self.inputBackVideo)

    def save_frame(self, frame):
        print("detect!!")
        now = str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        cv2.imwrite(('C:/_workspace/main/main_server_v2.0/front_det/'+now+'.jpg'), frame)
        ...

