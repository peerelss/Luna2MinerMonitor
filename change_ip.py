import requests
import subprocess
import csv

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="dc1c0c71d06262975eb325bc6e0ab965", uri="/cgi-bin/set_network_conf.cgi", response="5b3f8963687cd6e97af55677233970b8", qop=auth, nc=00000027, cnonce="9d7823fcbad4345a"',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'http://11.8.4.91',
    'Referer': 'http://11.8.4.91/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def change_miner_ip(old_ip, new_ip):
    if len(old_ip) > 7 and len(new_ip) >= 7 and new_ip != old_ip:
        p_data = '{"ipHost":"Antminer","ipPro":2,"ipAddress":"' + new_ip + '","ipSub":"255.255.248.0","ipGateway":"11.8.7.254","ipDns":"8.8.8.8"}'
        try:
            response = requests.post('http://' + old_ip + '/cgi-bin/set_network_conf.cgi', headers=headers, data=p_data,
                                     verify=False)
            print(response.json())
            response.raise_for_status()
            print(new_ip)
            print("Request was successful:", response.json())  # 假设返回的是 JSON 响应
        except requests.exceptions.ConnectionError:
            print("Error: Failed to connect to the server.")
        except requests.exceptions.Timeout:
            print("Error: Request timed out.")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    else:
        print(old_ip, new_ip)


def is_ip_online(ip):
    # 在 Windows 上使用 `-n 1`，在 Linux/macOS 上使用 `-c 1`
    command = ["ping", "-c", "1", ip]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return True  # 返回 True 表示在线
    except subprocess.CalledProcessError:
        return False  # 捕获异常表示不在线


def get_data_from_csv():
    data_p = []

    # 读取 CSV 文件
    with open(r'D:\csv\9-1.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data_p.append(row)
    return data_p


if __name__ == '__main__':
    data = get_data_from_csv()
    # 初始化一个空列表来存储二维数组

    for i in range(1, len(data)):
        change_miner_ip(data[i][1], data[i][3])
