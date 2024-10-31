import sys
import csv
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication

from miner_tools.tools import change_miner_ip, is_ip_online


def custom_function(param1, param2):
    # 在这里定义自定义函数的逻辑，例如简单地将两个参数连接
    if len(param1) > 7 and len(param2) > 7 and param2!=param1:
        result = change_miner_ip(param1, param2)
        return f"Processed ({param1}, {param2},{result}),"  # 示例处理逻辑
    else:
        return f"Processed ({param1}, {param2}),error"


class CSVViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CSV Viewer")
        self.setGeometry(300, 300, 1000, 1000)

        # 设置主布局
        layout = QtWidgets.QVBoxLayout()

        # 输入框用于显示CSV文件路径
        self.path_input = QtWidgets.QLineEdit(self)
        self.path_input.setPlaceholderText("Choose CSV file...")
        self.path_input.setReadOnly(True)
        self.path_input.setStyleSheet("padding: 8px; font-size: 14px;")

        # 文件选择按钮
        self.select_button = QtWidgets.QPushButton("Select CSV File", self)
        self.select_button.clicked.connect(self.select_csv_file)
        self.select_button.setStyleSheet("""
            background-color: #007ACC; color: white;
            padding: 8px; border-radius: 5px;
            font-size: 14px;
        """)

        # 显示CSV内容的文本框
        self.text_display = QtWidgets.QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("font-size: 14px; padding: 8px;")

        # 加载CSV内容按钮
        self.load_button = QtWidgets.QPushButton("Load CSV Content", self)
        self.load_button.clicked.connect(self.load_csv_content)
        self.load_button.setStyleSheet("""
            background-color: #28A745; color: white;
            padding: 8px; border-radius: 5px;
            font-size: 14px;
        """)

        # 执行函数按钮
        self.execute_button = QtWidgets.QPushButton("Execute Function on CSV Data", self)
        self.execute_button.clicked.connect(self.execute_function_on_csv)
        self.execute_button.setStyleSheet("""
            background-color: #FF5733; color: white;
            padding: 8px; border-radius: 5px;
            font-size: 14px;
        """)

        # 执行结果文本框
        self.result_display = QtWidgets.QTextEdit(self)
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("font-size: 14px; padding: 8px;")

        # 添加到布局
        layout.addWidget(self.path_input)
        layout.addWidget(self.select_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.text_display)
        layout.addWidget(self.result_display)

        # 设置主窗口布局
        self.setLayout(layout)

    def select_csv_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "",
                                                             "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.path_input.setText(file_path)
            self.text_display.clear()
            self.result_display.clear()

    def load_csv_content(self):
        file_path = self.path_input.text()
        if not file_path:
            self.text_display.setText("Please select a CSV file first.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                csv_content = ""
                for row in reader:
                    csv_content += ", ".join(row) + "\n"
                self.text_display.setText(csv_content)
        except Exception as e:
            self.text_display.setText(f"Failed to load CSV content: {str(e)}")

    def execute_function_on_csv(self):
        file_path = self.path_input.text()
        if not file_path:
            self.result_display.setText("Please select a CSV file first.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # 跳过表头行
                results = ""
                for row in reader:
                    if len(row) >= 4:  # 确保每行至少有四个元素
                        result = custom_function(row[1], row[3])
                        results += f"Result for {row[1]} and {row[3]}: {result}\n"
                        self.result_display.append(results)
                        QApplication.processEvents()  # 刷新文本框，立即显示当前结果
                self.result_display.setText(results)
        except Exception as e:
            self.result_display.setText(f"Error executing function: {str(e)}")


# 程序入口
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')  # 设置样式
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())
