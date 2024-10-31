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
            response.raise_for_status()
            print("Request was successful:", response.json())  # 假设返回的是 JSON 响应
            return response.json()
        except requests.exceptions.ConnectionError:
            print("Error: Failed to connect to the server.")
        except requests.exceptions.Timeout:
            print("Error: Request timed out.")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        return f"An error occurred: {old_ip}"


def is_ip_online(ip):
    # 在 Windows 上使用 `-n 1`，在 Linux/macOS 上使用 `-c 1`
    command = ["ping", "-c", "1", ip]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return True  # 返回 True 表示在线
    except subprocess.CalledProcessError:
        return False  # 捕获异常表示不在线
