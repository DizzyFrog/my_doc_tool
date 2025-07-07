# app.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QProgressBar, QLabel, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QMenuBar, QMenu, QMessageBox, QSplitter, QDialog, QFormLayout, QComboBox
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
from backend.mermaid_utils import is_mermaid_installed
import os
import pandas as pd
import shutil
from dotenv import load_dotenv, set_key
from backend.excel_utils import excel_utils

load_dotenv('.env',override=True)
from mylog.log import logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("结构化文档批处理工具")
        self.setWindowIcon(QIcon("favo.png"))
        self.resize(900, 600)
        self.init_ui()

    def init_ui(self):
        # 菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        settings_menu = menubar.addMenu("设置")
        help_menu = menubar.addMenu("帮助")

        # 文件菜单示例
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 主分区
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 左侧操作区
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(260)

        self.upload_btn = QPushButton("上传 Excel 文件")
        left_layout.addWidget(self.upload_btn)

        self.mermaid_btn = QPushButton("检查 Mermaid CLI")
        left_layout.addWidget(self.mermaid_btn)

        self.start_btn = QPushButton("开始批量处理")
        left_layout.addWidget(self.start_btn)

        self.settings_btn = QPushButton("系统设置")
        self.settings_btn.clicked.connect(self.open_settings)
        left_layout.addWidget(self.settings_btn)

        left_layout.addStretch()

        # 右侧内容区
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        

        self.progress_label = QLabel("处理进度/日志：")
        right_layout.addWidget(self.progress_label)
        self.progress_bar = QProgressBar()
        right_layout.addWidget(self.progress_bar)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        right_layout.addWidget(self.log_text)

        self.export_btn = QPushButton("导出 docx 文件")
        right_layout.addWidget(self.export_btn)

        # 主布局分区
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 3)
        main_layout.addWidget(splitter)

        self.mermaid_btn.clicked.connect(self.check_mermaid_cli)
        self.upload_btn.clicked.connect(self.upload_excel)

    def check_mermaid_cli(self):
        if is_mermaid_installed():
            QMessageBox.information(self, "检查结果", "Mermaid CLI 已安装！")
        else:
            QMessageBox.warning(self, "检查结果", "未检测到 Mermaid CLI，请先安装！")

    def open_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec():
            # 可在此处刷新主界面数据（如有需要）
            pass

    def upload_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            os.makedirs('data/input', exist_ok=True)
            new_path = os.path.join('data', 'input', 'input.xlsx')
            shutil.copy(file_path, new_path)
            sheets = excel_utils.get_excel_sheets()
            if not sheets:
                QMessageBox.warning(self, "错误", "无法读取Excel文件或没有sheet页！")
                return
            dlg = SheetSelectDialog(sheets, self)
            if dlg.exec():
                sheet_name = dlg.selected_sheet
                self.save_sheet_to_env(sheet_name)
                QMessageBox.information(self, "成功", f"已选择Sheet: {sheet_name}，并保存到.env")
                logger.info(f"已选择Sheet: {sheet_name}，并保存到.env")

    def save_sheet_to_env(self, sheet_name):
        set_key('.env', 'SHEET_NAME', sheet_name)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("系统设置")
        self.setModal(True)
        self.resize(400, 180)
        layout = QFormLayout(self)

        self.baseurl_input = QLineEdit()
        self.apikey_input = QLineEdit()
        self.apikey_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.model_input = QLineEdit()

        layout.addRow("Base URL：", self.baseurl_input)
        layout.addRow("API Key：", self.apikey_input)
        layout.addRow("Model Name：", self.model_input)

        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.save_env)
        layout.addRow(self.save_btn)

        self.load_env()

    def load_env(self):
        self.baseurl_input.setText(os.getenv('BASEURL', ''))
        self.apikey_input.setText(os.getenv('APIKEY', ''))
        self.model_input.setText(os.getenv('MODEL_NAME', ''))

    def save_env(self):
        set_key('.env', 'BASEURL', self.baseurl_input.text().strip())
        set_key('.env', 'APIKEY', self.apikey_input.text().strip())
        set_key('.env', 'MODEL_NAME', self.model_input.text().strip())
        QMessageBox.information(self, "保存成功", ".env 配置已保存！")
        
        self.accept()

class SheetSelectDialog(QDialog):
    def __init__(self, sheets, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择 Sheet")
        self.selected_sheet = None
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("请选择需要处理的 Sheet："))
        logger.info("请选择需要处理的 Sheet：")
        self.combo = QComboBox()
        self.combo.addItems(sheets)
        layout.addWidget(self.combo)
        btn = QPushButton("确定")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def accept(self):
        self.selected_sheet = self.combo.currentText()
        super().accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())