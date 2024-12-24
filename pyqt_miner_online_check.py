import sys
import pandas as pd
import socket
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QFileDialog, QWidget, QGridLayout, QTextEdit
)

class FileGridApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.excel_data = None  # To store the loaded Excel data

    def init_ui(self):
        self.setWindowTitle("File Grid Example")
        self.setGeometry(100, 100, 600, 400)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # File input and button
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select a file...")
        file_button = QPushButton("Browse")
        file_button.clicked.connect(self.select_file)
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.read_file_content)
        all_button = QPushButton("All")
        all_button.clicked.connect(self.process_all_sheets)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)
        file_layout.addWidget(start_button)
        file_layout.addWidget(all_button)

        # Grid layout
        grid_layout = QGridLayout()
        self.grid_buttons = []

        button_number = 1
        for i in range(2):
            for j in range(8):
                if button_number == 4:
                    grid_layout.addWidget(QWidget(), i, j)  # Empty placeholder for Button 4
                elif button_number > 4:
                    button = QPushButton(f"Button {button_number - 1}")
                    grid_layout.addWidget(button, i, j)
                    self.grid_buttons.append(button)
                else:
                    button = QPushButton(f"Button {button_number}")
                    grid_layout.addWidget(button, i, j)
                    self.grid_buttons.append(button)
                button_number += 1

        # Assign actions to all buttons
        for idx, button in enumerate(self.grid_buttons):
            button.clicked.connect(lambda _, i=idx + 1: self.display_sheet(i))

        # Text box for file content
        self.file_content_display = QTextEdit()
        self.file_content_display.setReadOnly(True)

        # Add layouts to main layout
        main_layout.addLayout(file_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.file_content_display)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", filter="Excel Files (*.xls *.xlsx)")
        if file_path:
            self.file_input.setText(file_path)

    def read_file_content(self):
        file_path = self.file_input.text()
        if file_path:
            try:
                self.excel_data = pd.ExcelFile(file_path)
                self.file_content_display.setText("File loaded successfully. Select a button to view specific sheet content.")
            except Exception as e:
                self.file_content_display.setText(f"Error loading file: {e}")

    def is_ip_online(self, ip):
        try:
            socket.create_connection((ip, 80), timeout=2)
            return True
        except Exception:
            return False

    def display_sheet(self, sheet_number):
        self.file_content_display.clear()  # Clear the text box
        if self.excel_data is not None:
            sheet_name = f"{sheet_number}号厂房"
            try:
                if sheet_name in self.excel_data.sheet_names:
                    sheet_data = self.excel_data.parse(sheet_name)
                    # Filter rows where column C is not empty
                    filtered_data = sheet_data[sheet_data.iloc[:, 2].notna()]
                    if filtered_data.empty:
                        self.file_content_display.setText("No data found in column C.")
                        return

                    # Check IPs in column B
                    offline_ips = []
                    for ip in filtered_data.iloc[:, 1]:
                        if isinstance(ip, str) and self.is_ip_online(ip) is False:
                            offline_ips.append(ip)

                    if offline_ips:
                        self.file_content_display.setText("Offline IPs:\n" + "\n".join(offline_ips))
                    else:
                        self.file_content_display.setText("All IPs are online.")
                else:
                    self.file_content_display.setText(f"Sheet '{sheet_name}' not found in the file.")
            except Exception as e:
                self.file_content_display.setText(f"Error reading sheet: {e}")
        else:
            self.file_content_display.setText("No file loaded. Please load an Excel file first.")

    def process_all_sheets(self):
        self.file_content_display.clear()  # Clear the text box
        if self.excel_data is not None:
            results = []
            for sheet_number in range(1, 16):
                sheet_name = f"{sheet_number}号厂房"
                if sheet_name in self.excel_data.sheet_names:
                    try:
                        sheet_data = self.excel_data.parse(sheet_name)
                        # Filter rows where column C is not empty
                        filtered_data = sheet_data[sheet_data.iloc[:, 2].notna()]
                        if not filtered_data.empty:
                            # Check IPs in column B
                            offline_ips = []
                            for ip in filtered_data.iloc[:, 1]:
                                if isinstance(ip, str) and self.is_ip_online(ip) is False:
                                    offline_ips.append(ip)

                            if offline_ips:
                                results.append(f"{sheet_name} Offline IPs:\n" + "\n".join(offline_ips))
                    except Exception as e:
                        results.append(f"Error processing {sheet_name}: {e}")

            if results:
                self.file_content_display.setText("\n\n".join(results))
            else:
                self.file_content_display.setText("All sheets processed. No offline IPs found.")
        else:
            self.file_content_display.setText("No file loaded. Please load an Excel file first.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileGridApp()
    window.show()
    sys.exit(app.exec_())
