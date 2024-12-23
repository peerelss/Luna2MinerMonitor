import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QCheckBox

from PyQt5.QtCore import Qt, QTimer
import requests
from datetime import datetime
from pygame import mixer  # Load the popular external library

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="9c3e92338fe8940f082245e875f65539", uri="/cgi-bin/get_miner_conf.cgi", response="17162f48ebb89d29c01e33decd353c19", qop=auth, nc=00000042, cnonce="30f147bf532141fe"',
    'Connection': 'keep-alive',
    'Referer': 'http://10.7.0.1/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
ip_range = [0, 1, 2, 3]
ip_3 = [1, 2, 3, 6, 7, 8]


def get_box_mode(box_no):
    result = []
    for ip2 in ip_range:
        for ip3 in ip_3:
            result.append(get_miner_mode("10." + str(box_no) + '.' + str(ip2) + '.' + str(ip3)))
    count_0 = 0
    for r in result:
        if r == 0:
            count_0 = count_0 + 1
    if count_0 >= 10:
        return 0
    else:
        return -1


def get_miner_mode(ip):
    print(ip)
    try:
        response = requests.get('http://' + ip + '/cgi-bin/get_miner_conf.cgi', timeout=1, headers=headers,
                                verify=False).json()
        return int(response['bitmain-work-mode'])
    except requests.exceptions.ConnectionError:
        print("连接错误：无法连接到服务器")
    except requests.exceptions.Timeout:
        print("请求超时：服务器响应时间过长")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"请求错误：{req_err}")
    except ValueError:
        print("解析错误：返回的数据不是有效的JSON格式")
    except Exception as err:
        print(f"其他错误：{err}")
    return -1


class MiningStatusWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化网格布局
        self.layout = QGridLayout()

        # 创建10个矿箱的状态显示
        self.status_labels = []
        self.miner_ips = [6, 7, 8, 9, 10, 5, 2, 1, 3, 4]  # 矿箱
        self.miner_statues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(10):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(150, 150)  # 调整尺寸以适应更大的文字
            label.setStyleSheet("font-size: 24px;")  # 字体调大一倍
            self.status_labels.append(label)

            # 将矿箱放置在网格布局中
            row = i // 5  # 行号 (0 或 1)
            col = i % 5  # 列号 (0 到 4)
            self.layout.addWidget(label, row, col)

        # 添加一个标签来显示最后的更新时间
        self.time_label = QLabel("最后更新时间: 未知")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label, 2, 0, 1, 5)  # 放置在第三行，占满五列

        self.setLayout(self.layout)

        # 设置定时器，每5分钟更新一次
        self.update_status()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5 * 60 * 1000)  # 5分钟 (5 * 60 * 1000 毫秒)

    def update_status(self):
        for i, ip in enumerate(self.miner_ips):
            status = get_box_mode(ip)
            if status != self.miner_statues[i]:
                # 矿机状态改变
                print('box no status changed')
                play_music()
            self.miner_statues[i] = status
            if status == 0:
                self.status_labels[i].setStyleSheet("background-color: green;font-size: 24px; border-radius: 50px;")
                self.status_labels[i].setText(f"{i + 1}\n正常")

            else:
                self.status_labels[i].setStyleSheet("background-color: red;font-size: 24px; border-radius: 50px;")
                self.status_labels[i].setText(f"{i + 1}\n不正常")
                # mixer.init()
                # mixer.music.load('2216.mp3')
                # mixer.music.play()
        # 更新最后更新时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.time_label.setText(f"最后更新时间: {current_time}")
        self.time_label.setStyleSheet("font-size: 24px;")  # 字体调大一倍


def play_music():
    mixer.init()
    mixer.music.load('2216.mp3')
    mixer.music.play()


def main():
    app = QApplication(sys.argv)

    window = MiningStatusWidget()
    window.setWindowTitle("矿箱状态监控")
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
