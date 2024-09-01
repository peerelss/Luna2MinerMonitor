import tkinter as tk
from datetime import datetime

import requests
import winsound

window = tk.Tk()
t = tk.Text(window, )
t.pack(fill='both', padx='5px', pady='5px')
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="44eacc09ef6288030ff133746af0b22e", uri="/cgi-bin/summary.cgi", response="e07e9fd64382fe34462232de2b98efd4", qop=auth, nc=00000057, cnonce="31756743fce17bb0"',
    'Connection': 'keep-alive',
    'Referer': 'http://10.1.1.1/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

container_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ip_range = [0, 1, 2, 3]
ip_3 = [1, 2, 3, 6, 7, 8]


def get_miner_mode(ip):
    try:
        response = requests.get('http://' + ip + '/cgi-bin/stats.cgi', headers=headers, verify=False)
        return response.json()['STATS'][0]['miner-mode']
    except:
        return -1


def get_miner_conf(ip):
    response = requests.get('http://' + ip + '/cgi-bin/get_miner_conf.cgi', headers=headers, verify=False)
    mode_miner = response.json()['bitmain-work-mode']
    print(mode_miner)


def is_con_box_good(result):
    count_0 = 0
    for r in result:
        if r == 0:
            count_0 = count_0 + 1
    return count_0 >= 20


def find_miner_box(box_no):
    result = []
    for ip2 in ip_range:
        for ip3 in ip_3:
            result.append(get_miner_mode("10." + str(box_no) + '.' + str(ip2) + '.' + str(ip3)))
    if is_con_box_good(result):
        t.insert('insert', str(box_no) + " good " + "\n")
    else:
        t.insert('insert', str(box_no) + " not good " + "\n")

    # 判断每个矿箱里的机器的状态.


def find_miner_stats():
    # 记录状态
    t.delete('1.0', 'end')
    current_date_and_time = datetime.now()
    t.insert('insert', "The current date and time is " +str( current_date_and_time))
    for box_no in container_range:
        find_miner_box(box_no)


def task_miner():
    # 记录状态
    find_miner_stats()
    window.after(5 * 60 * 1000, task_miner)


if __name__ == "__main__":
    get_miner_conf('10.1.1.1')
    window.after(5 * 1000, task_miner)
    window.mainloop()
