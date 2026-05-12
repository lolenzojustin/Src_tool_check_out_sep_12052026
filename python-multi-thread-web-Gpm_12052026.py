import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from random import randint
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

import time
import urllib.request, json
import requests
import threading
import os
import random
import string
import re
import datetime
import shutil
import uiautomator2 as uc
from adbutils import adb
from dotenv import load_dotenv, set_key
import GpmGlobalApi_tuviet
from screeninfo import get_monitors

# ===========================
# UI GIAO DIỆN CHÍNH
# ===========================
class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1499, 925)
        self.verticalLayoutWidget = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-10, 0, 1511, 701))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.startBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.startBtn.setStyleSheet("#startBtn {\n"
"    background-color: white;       /* nền trắng */\n"
"    color: black;                  /* chữ đen */\n"
"    border: 2px solid black;       /* viền đen đậm */\n"
"    border-radius: 5px;            /* bo góc mềm mại */\n"
"    font: 800 12pt \"Segoe UI\";     /* font Segoe UI, đậm, 10pt */\n"
"    font-weight: bold;             /* đảm bảo đậm rõ */\n"
"}\n"
"\n"
"#startBtn:hover {\n"
"    background-color: #f0f0f0;     /* nền xám nhạt khi hover */\n"
"    border: 2px solid black;       /* giữ viền đen */\n"
"    color: black;                  /* chữ vẫn đen */\n"
"}\n"
"")
        self.startBtn.setObjectName("startBtn")
        self.verticalLayout.addWidget(self.startBtn)
        self.stopBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stopBtn.setStyleSheet("#stopBtn {\n"
"    background-color: white;       /* nền trắng */\n"
"    color: black;                  /* chữ đen */\n"
"    border: 2px solid black;       /* viền đen đậm */\n"
"    border-radius: 5px;            /* bo góc mềm mại */\n"
"    font: 800 12pt \"Segoe UI\";     /* font Segoe UI, đậm, 10pt */\n"
"    font-weight: bold;             /* đảm bảo đậm rõ */\n"
"}\n"
"\n"
"#stopBtn:hover {\n"
"    background-color: #f0f0f0;     /* nền xám nhạt khi hover */\n"
"    border: 2px solid black;       /* giữ viền đen */\n"
"    color: black;                  /* chữ vẫn đen */\n"
"}\n"
"")
        self.stopBtn.setObjectName("stopBtn")
        self.verticalLayout.addWidget(self.stopBtn)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(260, 740, 381, 171))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_2.setStyleSheet("background-color: rgb(0, 170, 255);\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_4.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_2.addWidget(self.lineEdit_4)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.comboBox_2.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 0, 0);   /* đỏ tươi */\n"
"    border: 1px solid gray;\n"
"    font: 700 9pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* nếu muốn list xổ xuống cũng hơi đỏ đỏ */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(255, 100, 100);\n"
"}\n"
"")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_6.setStyleSheet("background-color: rgb(0, 170, 0);\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.verticalLayout_2.addWidget(self.lineEdit_6)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(70, 740, 191, 171))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_10.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"background-color: rgb(0, 170, 255);")
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.verticalLayout_3.addWidget(self.lineEdit_10)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_12.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"background-color: rgb(255, 255, 0);")
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.verticalLayout_3.addWidget(self.lineEdit_12)
        self.comboBox_4 = QtWidgets.QComboBox(self.verticalLayoutWidget_3)
        self.comboBox_4.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 0, 0);   /* đỏ tươi */\n"
"    border: 1px solid gray;\n"
"    font: 700 9pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* nếu muốn list xổ xuống cũng hơi đỏ đỏ */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(255, 100, 100);\n"
"}\n"
"")
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.verticalLayout_3.addWidget(self.comboBox_4)
        self.lineEdit_23 = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_23.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"background-color: rgb(0, 170, 0);")
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.verticalLayout_3.addWidget(self.lineEdit_23)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(820, 730, 211, 171))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_14.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"background-color: rgb(0, 255, 0);")
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.verticalLayout_4.addWidget(self.lineEdit_14)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_15.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"background-color: rgb(255, 170, 0);")
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.verticalLayout_4.addWidget(self.lineEdit_15)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_17.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"\n"
"background-color: rgb(170, 85, 255);")
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.verticalLayout_4.addWidget(self.lineEdit_17)
        self.comboBox_5 = QtWidgets.QComboBox(self.verticalLayoutWidget_4)
        self.comboBox_5.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 0, 255);   /* đỏ tươi */\n"
"    border: 1px solid gray;\n"
"    font: 700 9pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* nếu muốn list xổ xuống cũng hơi đỏ đỏ */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(255, 0, 255);\n"
"}\n"
"")
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.verticalLayout_4.addWidget(self.comboBox_5)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        self.lineEdit_19.setStyleSheet("font: 700 9pt \"Segoe UI\";\n"
"\n"
"background-color: rgb(85, 85, 255);")
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.verticalLayout_4.addWidget(self.lineEdit_19)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Widget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(1030, 730, 381, 171))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.lineEdit_13.setStyleSheet("background-color: rgb(0, 255, 0);\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.verticalLayout_5.addWidget(self.lineEdit_13)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.lineEdit_16.setStyleSheet("background-color: rgb(255, 170, 0);\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.verticalLayout_5.addWidget(self.lineEdit_16)
        self.lineEdit_20 = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.lineEdit_20.setStyleSheet("background-color: rgb(170, 85, 255);\n"
"\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.verticalLayout_5.addWidget(self.lineEdit_20)
        self.comboBox_3 = QtWidgets.QComboBox(self.verticalLayoutWidget_5)
        self.comboBox_3.setStyleSheet("QComboBox {\n"
"    background-color: rgb(255, 0, 255);   /* đỏ tươi */\n"
"    border: 1px solid gray;\n"
"    font: 700 9pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* nếu muốn list xổ xuống cũng hơi đỏ đỏ */\n"
"QComboBox QAbstractItemView {\n"
"    background-color: rgb(255, 0, 255);\n"
"}\n"
"")
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.verticalLayout_5.addWidget(self.comboBox_3)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.verticalLayoutWidget_5)
        self.lineEdit_22.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"\n"
"font: 700 9pt \"Segoe UI\";")
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.verticalLayout_5.addWidget(self.lineEdit_22)
        self.comboBox = QtWidgets.QComboBox(Widget)
        self.comboBox.setGeometry(QtCore.QRect(258, 720, 381, 26))
        self.comboBox.setStyleSheet("\n"
"font: 700 9pt \"Segoe UI\";")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit_5 = QtWidgets.QLineEdit(Widget)
        self.lineEdit_5.setGeometry(QtCore.QRect(70, 720, 191, 26))
        self.lineEdit_5.setStyleSheet("font: 700 9pt \"Segoe UI\";")
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Widget", "Proxy"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Widget", "Email"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Widget", "Mật khẩu"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Widget", "Tháng sinh nhật"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Widget", "Trạng Thái"))
        self.startBtn.setText(_translate("Widget", "Bắt đầu"))
        self.stopBtn.setText(_translate("Widget", "Dừng"))
        self.comboBox_2.setItemText(0, _translate("Widget", "1"))
        self.comboBox_2.setItemText(1, _translate("Widget", "2"))
        self.comboBox_2.setItemText(2, _translate("Widget", "3"))
        self.comboBox_2.setItemText(3, _translate("Widget", "4"))
        self.comboBox_2.setItemText(4, _translate("Widget", "5"))
        self.comboBox_2.setItemText(5, _translate("Widget", "6"))
        self.comboBox_2.setItemText(6, _translate("Widget", "7"))
        self.comboBox_2.setItemText(7, _translate("Widget", "8"))
        self.comboBox_2.setItemText(8, _translate("Widget", "9"))
        self.comboBox_2.setItemText(9, _translate("Widget", "10"))
        self.comboBox_2.setItemText(10, _translate("Widget", "11"))
        self.comboBox_2.setItemText(11, _translate("Widget", "12"))
        self.comboBox_2.setItemText(12, _translate("Widget", "Dec"))
        self.lineEdit_10.setText(_translate("Widget", "Mail Domain ->"))
        self.lineEdit_12.setText(_translate("Widget", "Mật Khẩu ->"))
        self.comboBox_4.setItemText(0, _translate("Widget", "Số Luồng ( Chọn số ->)"))
        self.lineEdit_23.setText(_translate("Widget", "API Captra ->>>"))
        self.lineEdit_14.setText(_translate("Widget", "Phiên Bản Trình Duyệt"))
        self.lineEdit_15.setText(_translate("Widget", "Phiên bản tool"))
        self.lineEdit_17.setText(_translate("Widget", "File.txt Danh Sách Proxy"))
        self.comboBox_5.setItemText(0, _translate("Widget", "Kích Thước Màn Hình ->"))
        self.lineEdit_19.setText(_translate("Widget", "API URL ( Nhập ->)"))
        self.comboBox_3.setItemText(0, _translate("Widget", "400,400"))
        self.comboBox_3.setItemText(1, _translate("Widget", "500,500"))
        self.comboBox_3.setItemText(2, _translate("Widget", "500,600"))
        self.comboBox_3.setItemText(3, _translate("Widget", "550,550"))
        self.comboBox_3.setItemText(4, _translate("Widget", "550,650"))
        self.comboBox_3.setItemText(5, _translate("Widget", "580,680"))
        self.comboBox_3.setItemText(6, _translate("Widget", "600,600"))
        self.comboBox_3.setItemText(7, _translate("Widget", "600,700"))
        self.comboBox_3.setItemText(8, _translate("Widget", "600,750"))
        self.comboBox_3.setItemText(9, _translate("Widget", "650,650"))
        self.comboBox_3.setItemText(10, _translate("Widget", "650,700"))
        self.comboBox_3.setItemText(11, _translate("Widget", "700,700"))
        self.comboBox_3.setItemText(12, _translate("Widget", "700,800"))
        self.comboBox_3.setItemText(13, _translate("Widget", "700,850"))
        self.comboBox_3.setItemText(14, _translate("Widget", "750,850"))
        self.comboBox_3.setItemText(15, _translate("Widget", "800,800"))
        self.comboBox_3.setItemText(16, _translate("Widget", "800,850"))
        self.comboBox_3.setItemText(17, _translate("Widget", "800,900"))
        self.comboBox_3.setItemText(18, _translate("Widget", "900,900"))
        self.comboBox_3.setItemText(19, _translate("Widget", "900,1050"))
        self.comboBox_3.setItemText(20, _translate("Widget", "1000,1000"))
        self.comboBox_3.setItemText(21, _translate("Widget", "1200,1200"))
        self.comboBox_3.setItemText(22, _translate("Widget", "1200,1300"))
        self.comboBox_3.setItemText(23, _translate("Widget", "1200,1400"))
        self.comboBox.setItemText(0, _translate("Widget", "Jan"))
        self.comboBox.setItemText(1, _translate("Widget", "Feb"))
        self.comboBox.setItemText(2, _translate("Widget", "Mar"))
        self.comboBox.setItemText(3, _translate("Widget", "Apr"))
        self.comboBox.setItemText(4, _translate("Widget", "May"))
        self.comboBox.setItemText(5, _translate("Widget", "Jun"))
        self.comboBox.setItemText(6, _translate("Widget", "Jul"))
        self.comboBox.setItemText(7, _translate("Widget", "Aug"))
        self.comboBox.setItemText(8, _translate("Widget", "Sep"))
        self.comboBox.setItemText(9, _translate("Widget", "Oct"))
        self.comboBox.setItemText(10, _translate("Widget", "Nov"))
        self.comboBox.setItemText(11, _translate("Widget", "Dec"))
        self.lineEdit_5.setText(_translate("Widget", "Tháng sinh nhật  ->"))


# ===========================
# THREAD MỖI LUỒNG GPM + PLAYWRIGHT
# ===========================
class MultiThread(QThread):
    # record: row_index, proxy, email, password, month, status
    record = pyqtSignal(object, object, object, object, object, object)

    def __init__(self, index, soluong, domain, password, month, proxy_list, apiurl, kichthuocmanhinh, api_captra):
        super().__init__()
        self.index = index
        self.soluong = soluong
        self.domain = domain
        self.password = password
        self.month = month
        self.proxy_list = proxy_list  # Lưu lại toàn bộ danh sách proxy
        self.proxy = None             # Proxy hiện tại sẽ được chọn sau
        self.apiurl = apiurl
        self.kichthuocmanhinh = kichthuocmanhinh
        self.api_captra = api_captra
        self.is_running = True

        self.gpm = None          # object GpmApi.Gpm()
        self.id_profile = None   # id profile do GPM tạo ra

    def calc_window_position(self, index, kichthuoc: str):
        width_ui, height_ui = map(int, kichthuoc.split(","))
        m = get_monitors()[0]
        screen_width = m.width

        so_luong_cot = screen_width // width_ui
        x = width_ui * (index % so_luong_cot) + 30
        y = (index // so_luong_cot) * height_ui + 30

        toado = f"{x},{y}"
        print("kích thước màn hình là", screen_width)
        print("toado là", toado)
        return toado

    def run(self):
        # Cho phép dừng mềm bằng is_running
        while self.is_running:
            try:
                # Bước 0: báo sẵn sàng
                self.record.emit(self.index, self.proxy, "-", "-", "-", "Sẵn sàng")
                self.CreateAcc()
            except Exception as e:
                print(f"Lỗi def run (thread {self.index}):", e)

            if not self.is_running:
                break

            time.sleep(2)

    def CreateAcc(self):
        start_time = time.time()
        account_created = False
        # ===> CHỌN PROXY NGẪU NHIÊN TẠI ĐÂY <===
        # Mỗi lần hàm CreateAcc được gọi (vòng lặp mới), nó sẽ lấy proxy mới
        import random
        self.proxy = random.choice(self.proxy_list)
        # =========================================
        random_email = "-"

        # Nếu self.month rỗng thì default là "Sep"
        text_month = self.month

        # Map tháng dạng "Jan", "Feb"... sang số 1–12
        month_map = {
            "Jan": "1",
            "Feb": "2",
            "Mar": "3",
            "Apr": "4",
            "May": "5",
            "Jun": "6",
            "Jul": "7",
            "Aug": "8",
            "Sep": "9",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }

        # Giá trị này sẽ dùng cho select_option
        select_option_month = month_map.get(text_month)  # chọn select_option_month theo giá trị value của text_month

        
        try:
            captra_nopecha = self.api_captra
            local_part = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            # local_part = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(25))
            # local_part = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))+ text_month
            mail_domain = self.domain
            random_email = f"{local_part}@{mail_domain}"
            toado = self.calc_window_position(self.index, self.kichthuocmanhinh)
            print(f"index {self.index} có tọa độ là {toado}")
            text_month = self.month if self.month else "Sep"

            list_text = list(string.ascii_lowercase)
            random_firstphone = ['361', '503', '971', '218', '781', '309']

            random_name = "".join(random.choice(list_text) for _ in range(5))
            list_zipcode = ['97266', '97215', '97220', '97071', '97045', '97288', '97233', '03010', '97035']
            random_zipcode = random.choice(list_zipcode)
            password_nhap = self.password

            # Bước 1: đã có email + pass, chuẩn bị tạo profile
            self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Chuẩn bị tạo profile")

            self.gpm = GpmGlobalApi_tuviet.Gpm()

            if self.proxy == "0" or self.proxy == 0:
                self.id_profile = self.gpm.create_profile_2(self.apiurl)
            else:
                self.id_profile = self.gpm.create_profile(self.apiurl, self.proxy)
            print("proxy là", self.proxy)
            print(f"Thread {self.index}: id_profile là {self.id_profile}")
            time.sleep(1)


            time.sleep(1)

            remote_debugging_address = self.gpm.open_profile(
                self.apiurl,
                self.id_profile,
                win_pos=f"{toado}",
                win_size=f"{self.kichthuocmanhinh}"
            )
            time.sleep(1)

            # Bước 3: đã mở profile GPM
            self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Đã mở profile GPM")

            wsUrl_Gpm = f"http://{remote_debugging_address}/json/version"
            with sync_playwright() as p:
                print("wsUrl_Gpm là", wsUrl_Gpm)
                browser = p.chromium.connect_over_cdp(endpoint_url=wsUrl_Gpm)

                # Bước 4: kết nối Playwright xong
                self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Kết nối Playwright xong")

                df_context = browser.contexts[0]
                page = df_context.pages[0]

                # Mở nopecha
                page.goto(
                    f"https://nopecha.com/setup#awscaptcha_auto_open=false|awscaptcha_auto_solve=false|awscaptcha_solve_delay=true|awscaptcha_solve_delay_time=1000|disabled_hosts=|enabled=true|funcaptcha_auto_open=true|funcaptcha_auto_solve=true|funcaptcha_solve_delay=true|funcaptcha_solve_delay_time=1000|geetest_auto_open=false|geetest_auto_solve=false|geetest_solve_delay=true|geetest_solve_delay_time=1000|hcaptcha_auto_open=true|hcaptcha_auto_solve=true|hcaptcha_solve_delay=true|hcaptcha_solve_delay_time=3000|{captra_nopecha}|keys=|lemincaptcha_auto_open=false|lemincaptcha_auto_solve=false|lemincaptcha_solve_delay=true|lemincaptcha_solve_delay_time=1000|perimeterx_auto_solve=false|perimeterx_solve_delay=true|perimeterx_solve_delay_time=1000|recaptcha_auto_open=true|recaptcha_auto_solve=true|recaptcha_solve_delay=true|recaptcha_solve_delay_time=2000|textcaptcha_auto_solve=false|textcaptcha_image_selector=|textcaptcha_input_selector=|textcaptcha_solve_delay=true|textcaptcha_solve_delay_time=100|turnstile_auto_solve=true|turnstile_solve_delay=true|turnstile_solve_delay_time=5000",
                    wait_until="domcontentloaded"
                )
                time.sleep(3)
                print("api_captra là ", captra_nopecha)

                # Mở trang Orders
                page.goto(
                    "https://www.sephora.com/profile/MyAccount/Orders",
                    wait_until="domcontentloaded"
                )

                # Bước 5: đã vào trang Orders
                self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Đang mở trang Orders")

                try:
                    page.wait_for_selector("text=Create Account", timeout=60000)
                    print("Đã thấy nút/tiêu đề Create Account, chạy bước tiếp theo...")
                except PlaywrightTimeoutError:
                    print("Không thấy 'Create Account' trong 60s")

                print("random_mail là", random_email)

                # Bước 6: bắt đầu reg tài khoản
                self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Bắt đầu reg tài khoản")

                page.get_by_role("button", name="Create Account").click()
                time.sleep(3)
                page.locator('//*[@id="email"]').fill(random_email)
                # time.sleep(1000)
                try:
                    page.get_by_text("Check Your Email", exact=True).wait_for(timeout=5000)
                    print("Nhập lại mail")
                    page.locator('//*[@data-at="modal_close"]').click()
                    time.sleep(2)
                    page.locator('//*[@data-at="sign_in_header"]').click()
                    time.sleep(2)
                    page.locator('//*[@data-at="create_account_button"]').click()
                    time.sleep(2)
                    page.locator('//*[@id="email"]').fill(random_email)
                    time.sleep(3)
                except PlaywrightTimeoutError:
                    print("Tiếp tục reg acc")

                page.get_by_role("button", name="Continue").click()
                time.sleep(5)
                page.locator('//*[@id="firstName"]').fill(random_name)
                time.sleep(3)
                page.locator('//*[@id="lastName"]').fill(random_name)
                time.sleep(3)
                page.locator('//*[@id="register_password"]').fill(password_nhap)
                time.sleep(3)

                page.locator('//*[@id="biRegMonth"]').select_option(select_option_month)
                random_day = str(random.randint(1, 29))
                page.locator('//*[@id="biRegDay"]').select_option(random_day)
                time.sleep(2)

                # Bước 7: form đã điền xong
                self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Điền form xong, gửi đăng ký")

                page.get_by_role("button", name="Join Now").click()


                check_disappear_locator = page.get_by_text("Enter your birthday to receive a free gift every year.")

                # success_text_locator = page.get_by_text("You have no recent orders.", exact=True)

                try:              
                    # success_text_locator.wait_for(state="visible", timeout=50000)

                    # state="hidden": Đợi cho text này BIẾN MẤT (ẩn đi hoặc bị xóa khỏi DOM)
                    check_disappear_locator.wait_for(state="hidden", timeout=50000)
                    
                    print("Text birthday đã biến mất, coi như đăng ký thành công bước 1.")
                    time.sleep(3) # Đợi thêm chút để page load ổn định

                    time.sleep(3)
                    if mail_domain == "gmail.com":
                        print("Tiếp Tục")
                        page.goto(
                            "https://www.sephora.com/profile/MyAccount",
                            wait_until="domcontentloaded"
                        )

                        try:
                            page.wait_for_selector("text=Account Information", timeout=60000)
                            print("Đã thấy Account Information, chạy bước tiếp theo...")
                        except PlaywrightTimeoutError:
                            print("Không thấy 'Account Information' trong 60s")

                        page.locator('//*[@data-at="myaccount_edit_button"]').click()
                        time.sleep(2)
                        page.locator('//*[@id="myaccount_email"]').fill(local_part + "@lolenzo.com")
                        time.sleep(2)
                        page.locator('//*[@id="myaccount_confirm_email"]').fill(local_part + "@lolenzo.com")
                        time.sleep(2)
                        page.get_by_role("button", name="Update").click()
                    else:
                        print("Kết thúc")

                    # Ghi file acc
                    with open("sephora_accounts.txt", "a", encoding="utf-8") as f:
                        f.write(f"{random_email}|{password_nhap}\n")
                    print("Đã lưu vào sephora_accounts.txt")
                    time.sleep(3)
                    time.sleep(1)
                    account_created = True

                    # Bước cuối: thành công
                    self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Thành công")

                except PlaywrightTimeoutError:
                    print("Không reg acc đc")
                    self.record.emit(self.index, self.proxy, random_email, password_nhap, text_month, "Không reg được")

                finally:
                    browser.close()
                    if mail_domain == "gmail.com":
                        print("Tiếp Tục với gmail.com ")
                    else:
                        print("tắt browser.close")

        except Exception as e:
            print("Lỗi trong CreateAcc:", e)
            email_show = random_email if random_email else "-"
            month_show = text_month if text_month else "-"
            try:
                self.record.emit(self.index, self.proxy, email_show, "Thang@123", month_show, "Tạo lỗi")
            except Exception as e2:
                print("Lỗi khi emit UI trong except CreateAcc:", e2)

        finally:
            elapsed = time.time() - start_time
            if (not account_created) and elapsed >= 180:
                print(f"⚠ Không tạo xong tài khoản trong 3 phút, đóng profile {self.id_profile}")
            else:
                print(f"Đóng profile {self.id_profile} (đã tạo xong hoặc dưới 3 phút)")

            if self.gpm is not None and self.id_profile is not None:
                try:
                    self.gpm.close_profile(self.apiurl, self.id_profile)
                    print("Đóng ở finally cuối")
                    print("Đóng id_profile", self.id_profile)
                    time.sleep(1)
                    self.gpm.update_profile(self.apiurl, self.id_profile)
                    print("Update id_profile", self.id_profile)
                    time.sleep(1)
                    self.gpm.delete_profile(self.apiurl, self.id_profile)
                    print("Delete id_profile", self.id_profile)
                    time.sleep(1)
                except Exception as e:
                    print("Lỗi khi close/update/delete profile:", e)

    def logOut(self):
        print("Bắt đầu logout")
        time.sleep(1)

    # def stop(self):
    #     # Chỉ đánh dấu dừng, để CreateAcc chạy đến finally tự close profile
    #     self.is_running = False
    #     print(f"Yêu cầu dừng thread {self.index}")
    def stop(self):
        # đánh dấu là đã được yêu cầu dừng
        self.is_running = False

        # 👉 ĐÓNG + XÓA PROFILE GPM
        try:
                if self.gpm is not None and self.id_profile is not None:
                # đóng profile
                        self.gpm.close_profile(self.apiurl, self.id_profile)
                        print(f"Đã đóng profile {self.id_profile}")

                        # xóa profile
                        self.gpm.delete_profile(self.apiurl, self.id_profile)
                        print(f"Đã xóa profile {self.id_profile}")
                else:
                        print(f"Thread {self.index}: không có profile để đóng/xóa")
        except Exception as e:
                print(f"Lỗi khi đóng/xóa profile {self.id_profile}: {e}")

        # cuối cùng mới kill thread
        self.terminate()

# ===========================
# MANAGER: GẮN UI + THREAD
# ===========================
class Manager(QtWidgets.QMainWindow, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.threads = []

        self.startBtn.clicked.connect(self.startThread)
        self.stopBtn.clicked.connect(self.stopThread)

        # Nghe thay đổi và lưu vào config.env
        self.lineEdit_2.textChanged.connect(lambda: self.updateConfig("lineEdit_2"))
        self.lineEdit_4.textChanged.connect(lambda: self.updateConfig("lineEdit_4"))
        self.comboBox_2.currentIndexChanged.connect(lambda: self.updateConfig("comboBox_2"))
        self.comboBox.currentIndexChanged.connect(lambda: self.updateConfig("comboBox"))
        self.lineEdit_6.textChanged.connect(lambda: self.updateConfig("lineEdit_6"))
        self.lineEdit_20.textChanged.connect(lambda: self.updateConfig("lineEdit_20"))
        self.comboBox_3.currentIndexChanged.connect(lambda: self.updateConfig("comboBox_3"))
        self.lineEdit_22.textChanged.connect(lambda: self.updateConfig("lineEdit_22"))

        # Load config.env
        self.env_file = "config.env"
        load_dotenv(self.env_file, encoding='utf-8')

        if os.getenv("MAIL_DOMAIN"):
            self.lineEdit_2.setText(os.getenv("MAIL_DOMAIN"))
        if os.getenv("PASSWORD"):
            self.lineEdit_4.setText(os.getenv("PASSWORD"))
        if os.getenv("THREADS"):
            self.comboBox_2.setCurrentText(os.getenv("THREADS"))
        if os.getenv("MONTH"):
            self.comboBox.setCurrentText(os.getenv("MONTH"))
        if os.getenv("captra"):
            self.lineEdit_6.setText(os.getenv("captra"))
        if os.getenv("fileproxy"):
            self.lineEdit_20.setText(os.getenv("fileproxy"))
        if os.getenv("kichthuocmanhinh"):
            self.comboBox_3.setCurrentText(os.getenv("kichthuocmanhinh"))
        if os.getenv("apiurl"):
            self.lineEdit_22.setText(os.getenv("apiurl"))

    def updateConfig(self, text):
        if text == "lineEdit_2":
            set_key(self.env_file, "MAIL_DOMAIN", self.lineEdit_2.text())
        if text == "lineEdit_4":
            set_key(self.env_file, "PASSWORD", self.lineEdit_4.text())
        if text == "comboBox_2":
            set_key(self.env_file, "THREADS", self.comboBox_2.currentText())
        if text == "comboBox":
            set_key(self.env_file, "MONTH", self.comboBox.currentText())
        if text == "lineEdit_6":
            set_key(self.env_file, "captra", self.lineEdit_6.text())
        if text == "lineEdit_20":
            set_key(self.env_file, "fileproxy", self.lineEdit_20.text())
        if text == "comboBox_3":
            set_key(self.env_file, "kichthuocmanhinh", self.comboBox_3.currentText())
        if text == "lineEdit_22":
            set_key(self.env_file, "apiurl", self.lineEdit_22.text())

    def startThread(self):
        # Không cho start nếu còn thread đang chạy
        if any(t.isRunning() for t in self.threads):
            QMessageBox.warning(self, "Đang chạy", "Vui lòng Dừng luồng cũ trước khi Bắt đầu lại.")
            return

        input_domain = self.lineEdit_2.text().strip()
        input_password = self.lineEdit_4.text().strip()
        input_month = self.comboBox.currentText().strip()
        input_soluong = int(self.comboBox_2.currentText())
        input_captra = self.lineEdit_6.text().strip()
        input_fileproxy = self.lineEdit_20.text().strip()
        input_kichthuocmanhinh = self.comboBox_3.currentText().strip()
        input_apiurl = self.lineEdit_22.text().strip()

        if not os.path.isfile(input_fileproxy):
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy file proxy: {input_fileproxy}")
            return

        with open(input_fileproxy, "r", encoding="utf-8") as file:
            content = file.readlines()
            proxyList = [line.strip() for line in content if line.strip()]

        # if len(proxyList) < input_soluong:
        #     QMessageBox.warning(self, "Lỗi", f"Số proxy trong file ({len(proxyList)}) < số luồng ({input_soluong})")
        #     return

        self.tableWidget.setRowCount(input_soluong)
        self.threads = []

        for i in range(input_soluong):
            thread = MultiThread(
                index=i,
                soluong=input_soluong,
                domain=input_domain,
                password=input_password,
                month=input_month,
                # proxy=random.choice(proxyList), 
                proxy_list=proxyList,  # <--- TRUYỀN CẢ LIST VÀO ĐÂY (Đổi tên tham số cho rõ)
                apiurl=input_apiurl,
                kichthuocmanhinh=input_kichthuocmanhinh,
                api_captra=input_captra
            )
            thread.record.connect(self.write_data)
            self.threads.append(thread)
            thread.start()
            time.sleep(0.5)

    def stopThread(self):
        # 1. Dừng toàn bộ thread đang chạy
        for t in self.threads:
                t.stop()   # trong stop() sẽ tự đóng profile
                t.wait()   # đợi thread đó kết thúc hẳn (optional nhưng nên có)

        # 2. Xóa danh sách thread, KHÔNG tắt tool
        self.threads = []
        # KHÔNG gọi QApplication.quit() hay QCoreApplication.instance().quit()

    def write_data(self, i, proxy, email, password, month_birthday, status):
        self.tableWidget.setItem(i, 0, QTableWidgetItem(str(proxy)))
        self.tableWidget.setItem(i, 1, QTableWidgetItem(str(email)))
        self.tableWidget.setItem(i, 2, QTableWidgetItem(str(password)))
        self.tableWidget.setItem(i, 3, QTableWidgetItem(str(month_birthday)))
        self.tableWidget.setItem(i, 4, QTableWidgetItem(str(status)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Manager()
    window.show()
    sys.exit(app.exec_())
