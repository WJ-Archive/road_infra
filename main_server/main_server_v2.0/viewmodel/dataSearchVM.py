# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from view.dataSearchView import DataSearchView
from model.db import mysql_lib # 추가

class DataSearchVM(QObject):
    def __init__(self, view: DataSearchView):
        """
        DataSearchVM Constructor
        @params: view(DataSearchView)
        """
        super().__init__()
        self.data_search_view = view
        self.dbh = mysql_lib.DB_Handler() # 추가
        # self.latitude = 0.0
        # self.longitude = 0.0

        # TODO: DB 연결
        data_object = [[]]
        self.data_search_view.data_result_tb.setRowCount(11)
        self.data_search_view.data_result_tb.setRowCount(100)
        self.data_search_view.search_btn.clicked.connect(self._searchDataInDB)

    def _searchDataInDB(self):
        """
        위도 및 경도 데이터를 DB에서 검색 후 해당 데이터를 위젯에 표기하는 메소드
        @params: None
        @return: None
        """
        # 변수 선언
        searched_data = None
        latitude = self.data_search_view.search_lat_le.text()
        longitude = self.data_search_view.search_lot_le.text()
        float_latitude = 0.0
        float_longitude = 0.0

        if latitude == "" and longitude == "":
            QMessageBox.warning(self.data_search_view, "입력 오류", "찾고자 하는 위도와 경도의 값이 모두 없습니다.", QMessageBox.Yes)
            return

        if latitude != "":
            print(latitude)
            float_latitude = float(latitude)

        if longitude != "":
            float_longitude = float(longitude)

        assert type(float_latitude) is float, logging.error("searchDataInDB 메소드의 latitude 인자 타입 오류")
        assert type(float_longitude) is float, logging.error("searchDataInDB 메소드의 longitude 인자 타입 오류")

        # 타입검사
        if type(float_latitude) is not float:
            logging.error("searchDataInDB 메소드의 latitude 인자 타입 오류")
            return
        if type(float_longitude) is not float:
            logging.error("searchDataInDB 메소드의 longitude 인자 타입 오류")
            return

        # TODO: DB 연결 후 검색
        if longitude == "":
            #print(latitude)
            searched_data = self.dbh.search(lat_q = latitude) # 추가
            pass
        elif latitude == "":
            #print(longitude)
            searched_data = self.dbh.search(lon_q = longitude) # 추가
            pass
        else:
            # searched_data = select * from DB table where latitude LIKE 'float_latitude%' and longitude LIKE 'float_longitude%'
            searched_data = self.dbh.search(latitude, longitude) # 추가
            pass

        #if searched_data is None:
            #QMessageBox.information(self.data_search_view, "데이터 오류", "찾고자 하는 데이터가 존재하지 않습니다.", QMessageBox.Yes)
        if len(searched_data) == 0:
            QMessageBox.information(self.data_search_view, "데이터 오류", "찾고자 하는 데이터가 존재하지 않습니다.", QMessageBox.Yes)
            return

        header = self.data_search_view.data_result_tb.horizontalHeader()
        row = len(searched_data)
        column_num = len(searched_data[0])
        self.data_search_view.data_result_tb.setRowCount(row)
        self.data_search_view.data_result_tb.setColumnCount(column_num)
        print(searched_data[0].keys())
        self.data_search_view.data_result_tb.setHorizontalHeaderLabels(searched_data[0].keys()) # 추가

        for row_idx in range(row):
            for col_no, (key, value) in enumerate(searched_data[row_idx].items()):
                #print(col_no)
                #print("key, valeuie",key,value)
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignHCenter)
                header.setSectionResizeMode(col_no, QHeaderView.ResizeToContents)
                
                self.data_search_view.data_result_tb.setItem(row_idx, col_no, item)

    def resizeFont(self, font_size: int) -> None:
        """
        data search view의 폰트 크기 변환 메소드
        params: font_size(int) - 글자크기
        return: None
        """
        assert type(font_size) is int, logging.error("인자가 int 타입이 아닙니다.")

        # 타입 검사
        if type(font_size) is not int:
            logging.error("인자가 int 타입이 아닙니다.")
            return

        # 폰트 설정
        font = self.data_search_view.lat_txt_lb.property("font")
        font.setPointSize(font_size)

        # view에 있는 폰트 변환 적용
        self.data_search_view.lat_txt_lb.setFont(font)
        self.data_search_view.lot_txt_lb.setFont(font)
        self.data_search_view.search_lat_le.setFont(font)
        self.data_search_view.search_lot_le.setFont(font)
        self.data_search_view.data_result_tb.setFont(font)
