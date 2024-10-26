import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound
from datetime import datetime

from miner_monitor_utils import get_container_box_ips


class MiningStatusWidget(QWidget):
    def __init__(self, config_file):
        super().__init__()

        # 从JSON文件加载配置
        self.miner_info = self.load_miner_config(config_file)
        self.rows = self.miner_info['rows']
        self.columns = self.miner_info['columns']
        self.miners = self.miner_info['miners']

        # 初始化布局
        self.layout = QVBoxLayout()
        self.grid_layout = QGridLayout()

        self.status_labels = []
        self.monitor_buttons = []
        self.miner_statuses = [None] * len(self.miners)  # 初始化矿箱状态列表

        # 创建矿箱的状态显示及切换按钮
        for miner in self.miners:
            container = QVBoxLayout()  # 使用垂直布局将状态标签和按钮组合在一起

            # 创建矿箱状态标签
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(150, 150)
            label.setStyleSheet("font-size: 24px;")
            self.status_labels.append(label)
            container.addWidget(label)  # 将状态标签添加到垂直布局中

            # 创建切换按钮
            button = QPushButton("加入检测" if miner['monitor'] else "退出检测")
            button.setCheckable(True)
            button.setChecked(miner['monitor'])
            button.setStyleSheet("font-size: 18px;")
            button.clicked.connect(lambda checked, index=self.miners.index(miner): self.toggle_monitor(index, checked))
            self.monitor_buttons.append(button)
            container.addWidget(button)  # 将切换按钮添加到垂直布局中

            # 将垂直布局添加到网格布局中
            self.grid_layout.addLayout(container, miner['row'], miner['col'])

        # 添加一个标签来显示最后的更新时间
        self.time_label = QLabel("最后更新时间: 未知")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.time_label)

        # 添加一个手动开关
        self.monitor_checkbox = QCheckBox("开启监听")
        self.monitor_checkbox.setStyleSheet("font-size: 24px;")
        self.monitor_checkbox.setChecked(False)
        self.monitor_checkbox.stateChanged.connect(self.toggle_monitoring)
        self.layout.addWidget(self.monitor_checkbox)

        # 布局组合
        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)

        # 初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)

        # 设置提示音
        self.alert_sound = QSound("alert.wav")

    def load_miner_config(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def toggle_monitor(self, index, checked):
        self.miners[index]['monitor'] = checked
        self.monitor_buttons[index].setText("加入检测" if checked else "退出检测")

    def toggle_monitoring(self, state):
        if state == Qt.Checked:
            self.update_status()  # 立即更新一次
            self.timer.start(5 * 60 * 1000)  # 每5分钟更新一次
        else:
            self.timer.stop()
            self.reset_status_labels()

    def update_status(self):
        for i, miner in enumerate(self.miners):
            if miner['monitor']:
                box_no = miner['id']
                ips = self.miner_info[box_no]
                normal_count = get_container_box_ips(ips)
                new_status = 0
                if normal_count * 100 / len(ips) > 60:
                    new_status = 0
                else:
                    new_status = -1
                if self.miner_statuses[i] is not None and self.miner_statuses[i] != new_status:
                    self.alert_sound.play()  # 状态变化时播放提示音

                self.miner_statuses[i] = new_status

                if new_status == 0:
                    self.status_labels[i].setStyleSheet(
                        "background-color: green; border-radius: 50px; font-size: 24px;")
                    self.status_labels[i].setText(f"编号: {miner['id']}\n  {normal_count}个正常")
                else:
                    self.status_labels[i].setStyleSheet("background-color: red; border-radius: 50px; font-size: 24px;")
                    self.status_labels[i].setText(f"编号: {miner['id']}\n  {normal_count}个正常")
            else:
                self.status_labels[i].setStyleSheet("background-color: gray; border-radius: 50px; font-size: 24px;")
                self.status_labels[i].setText(f"编号: {miner['id']}\n 未检测")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.time_label.setText(f"最后更新时间: {current_time}")

    def reset_status_labels(self):
        for i, label in enumerate(self.status_labels):
            label.setStyleSheet("background-color: gray; border-radius: 50px; font-size: 24px;")
            label.setText("待机")
            self.miner_statuses[i] = None


def main():
    app = QApplication(sys.argv)

    window = MiningStatusWidget('miner_config.json')
    window.setWindowTitle("矿箱状态监控")
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
