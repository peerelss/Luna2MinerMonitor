import pandas as pd

luna_b_path = r'C:\Users\MSI\Documents\luna\example_lunaB.xlsx'


def read_ips_form_xls(file_path):
    df = pd.read_excel(file_path, 'Sheet1')

    # 将数据框转为二维数组（嵌套列表）
    data = df.values.tolist()
    check_ips = [row[1] for row in data if len(row) > 1]
    # 打印结果
    return check_ips


def light_ip(ip):
    import requests
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'text/plain;charset=UTF-8',
            'Origin': 'http://11.4.0.3',
            'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="916414cff72e8d6c1b1433ab59cb6646", uri="/cgi-bin/blink.cgi", response="84c2ed2bf11329dc782a9b85dbbab8d7", qop=auth, nc=0000002f, cnonce="37203e3d903e8fde"',
            'Connection': 'keep-alive',
            'Referer': 'http://11.4.0.3/',
            'Priority': 'u=0',
        }

        data = '{"blink":true}'

        response = requests.post('http://' + ip + '/cgi-bin/blink.cgi', headers=headers, data=data)
        print(response.json())
        return ip + ' success'
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # 捕获非 requests 的其他异常
        return ip + ' failure'


if __name__ == '__main__':
    ips = read_ips_form_xls(luna_b_path)
    for ip in ips:
        print(light_ip(ip))
