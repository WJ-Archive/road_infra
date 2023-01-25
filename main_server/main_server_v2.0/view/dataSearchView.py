from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLineEdit, QLabel, QHBoxLayout, QAbstractItemView, QHeaderView, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

class DataSearchView(QWidget):
    def __init__(self, stylesheet="qss/dataSearchWin.qss"):
        super().__init__()
        self.lat_txt_lb = QLabel("위도 검색", objectName="lat_txt_lb")
        self.lot_txt_lb = QLabel("경도 검색", objectName="lot_txt_lb")
        self.search_lat_le = QLineEdit(objectName="search_lat_le")
        self.search_lot_le = QLineEdit(objectName="search_lot_le")
        self.data_result_tb = QTableWidget(self, objectName="data_result_tb")
        self.search_btn = QPushButton("검색", objectName="search_btn")

        double_validator = QDoubleValidator()
        self.search_lat_le.setValidator(double_validator)
        self.search_lot_le.setValidator(double_validator)

        self.data_result_tb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tb_header = self.data_result_tb.horizontalHeader()
        tb_header.setResizeMode(QHeaderView.Fixed)

        self.lat_txt_lb.setAlignment(Qt.AlignCenter)
        self.lot_txt_lb.setAlignment(Qt.AlignCenter)

        _vbox = QVBoxLayout()
        _hbox1 = QHBoxLayout()
        _hbox2 = QHBoxLayout()

        _hbox1.addWidget(self.lat_txt_lb, 1)
        _hbox1.addWidget(self.search_lat_le, 2)

        _hbox2.addWidget(self.lot_txt_lb, 1)
        _hbox2.addWidget(self.search_lot_le, 2)

        _vbox.addLayout(_hbox1, 1)
        _vbox.addLayout(_hbox2, 1)
        _vbox.addWidget(self.data_result_tb, 2)
        _vbox.addWidget(self.search_btn)
        self.setLayout(_vbox)

        self.setAttribute(Qt.WA_StyledBackground, True)

        with open(stylesheet, "r") as file:
            self.setStyleSheet(file.read())