import json
import requests

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="9c3e92338fe8940f082245e875f65539", uri="/cgi-bin/get_miner_conf.cgi", response="17162f48ebb89d29c01e33decd353c19", qop=auth, nc=00000042, cnonce="30f147bf532141fe"',
    'Connection': 'keep-alive',
    'Referer': 'http://10.7.0.1/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


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


def get_container_box_ips(ips):
    print(ips)
    result = []
    for ip in ips:
        result.append(get_miner_mode(ip))
    count_0 = 0
    for r in result:
        if r == 0:
            count_0 = count_0 + 1
    return count_0


def load_miner_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    conf_json = load_miner_config('miner_config.json')
    re = get_container_box_ips(conf_json['M4'])
    if re == 0:
        print('normal')
    else:
        print('not ')
