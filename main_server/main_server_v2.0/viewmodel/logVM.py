# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QObject

from view.logView import LogView


class LogVM(QObject):
    def __init__(self, view: LogView):
        """
        LogVM Constructor
        @params: view(LogView)
        """
        super().__init__()
        self.log_view = view
        self._model = None

        # TODO: 상수 및 변수 설정
        self._CACHE_SIZE = 1000
        self._cache_text = ""

        self._info_val_cnt = 0
        self._warn_val_cnt = 0
        self._err_val_cnt = 0
        #self._det_val_cnt = 0 #추가 (detect 된 객체 수)


    def resizeFont(self, font_size: int) -> None:
        """
        log view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
        return: None
        """
        assert type(font_size) is int, logging.error("인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int:
            logging.error("인자가 int 타입이 아닙니다.")
            return

        # 폰트 설정
        font = self.log_view.warn_txt.property("font")
        font.setPointSize(font_size)

        # view에 있는 폰트 변환 적용
        self.log_view.warn_txt.setFont(font)
        self.log_view.warn_val.setFont(font)
        self.log_view.err_txt.setFont(font)
        self.log_view.err_val.setFont(font)
        #self.log_view.det_txt.setFont(font) #추가
        #self.log_view.det_val.setFont(font) #추가

        self.log_view.txt_brw.setFont(font)


    def _countLogNo(self, log_type: str) -> None:
        """
        log 타입을 감지하여 log 타입에 따라 그 수를 증가하는 메소드

        @params: log_type(str) - 로그에 찍히는 데이터 타입
        @return: None
        """
        assert type(log_type) is str, logging.error("_countLogNo의 인자가 str 타입이 아닙니다.")

        if type(log_type) is not str:
            logging.error("_countLogNo의 인자가 str 타입이 아닙니다.")
            return

        # 로그 타입이 Warning 경우
        if log_type == "WARNING":
            self._warn_val_cnt += 1
            self.log_view.warn_val.setText(str(self._warn_val_cnt))
        # 로그타입이 에러인 경우
        elif log_type == "ERR":
            self._err_val_cnt += 1
            self.log_view.err_val.setText(str(self._err_val_cnt))
        #로그 타입이 Detect 인 경우
        #elif log_type == "DET":                                     #추가
        #    self._det_val_cnt += 1                                  #추가
        #    self.log_view.det_val.setText(str(self._det_val_cnt))   #추가
        #    ...
        # 그 외의 경우
        else:
            logging.error("없는 type입니다.")
            return


    def displayLog(self, log_type: str, msg: str) -> None:
        """
        로그 표시 메소드
        @params: log_type(str) - log 수준
                msg(str) - log 메시지
        @return: None
        """
        assert type(log_type) is str, logging.error("display 메소드의 log_type 인자가 string 타입이 아닙니다.")
        assert type(msg) is str, logging.error("display 메소드의 msg 인자가 string 타입이 아닙니다.")

        if type(log_type) is not str:
            logging.error("log_type 인자가 string 타입이 아닙니다.")
        elif type(msg) is not str:
            logging.error("msg 인자가 string 타입이 아닙니다.")
            return

        self.log_view.txt_brw.append(msg)

        # 로그타입 카운트
        self._countLogNo(log_type)

        # 화면 갱신 설정
        if len(self._cache_text) <= self._CACHE_SIZE:
            self._cache_text += msg
        else:
            self.log_view.txt_brw.clear()
            self._cache_text = ""