import requests
import concurrent.futures

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'multipart/form-data; boundary=---------------------------1659329941556934493644467265',
    'Origin': 'http://10.10.3.28',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="29f36f09b75b177d7b7295fb8faf90ff", uri="/cgi-bin/upgrade.cgi", response="959983435ee7e591d026383d5ea4744e", qop=auth, nc=00000043, cnonce="91d179a4ae2bee03"',
    'Connection': 'keep-alive',
    'Referer': 'http://10.10.3.28/',
}


def upgrade_ips(ip_pre, ip_begin, ip_end, file):
    for i in range(ip_begin, ip_end):
        upgrade_config_by_ip_and_file(ip_pre + str(i), file)


def upgrade_config_by_ip_and_file(ip, file):
    try:
        with open(file, 'rb') as f:
            files = {'firmware': (file, f, 'application/octet-stream')}
            response = requests.post('http://' + ip + '/cgi-bin/upgrade.cgi', headers=headers, files=files)
            print(ip,file)
            print(response.json())
    except Exception as e:
        print(f"请求错误: {e}")


def create_task(pre, begin, end, file):
    task_list = []
    for i in range(begin, end + 1):
        task_list.append([pre + str(i), file])
    return task_list


def up_fun(ips):
    upgrade_config_by_ip_and_file(ips[0], ips[1])


def parallel_process_2d(array_2d, func):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(func, array_2d))
    return results


if __name__ == '__main__':
    # upgrade_config_by_ip_and_file('10.10.3.1', './auth/30.auth')
   # upgrade_ips('10.10.3.', 51, 100, './auth/26.auth')
    task_ips = create_task('10.6.4.', 1, 60, './auth/13.auth')
    parallel_process_2d(task_ips, up_fun)
