import pandas as pd

luna_b_path = r'doa1.xlsx'


def get_blog_by_ip(ip):
    if len(str(ip)) > 7:
        import requests

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="7ccbaac3da135fb9922d1c98501d9a43", uri="/cgi-bin/dlog.cgi", response="fc4aed3aaec76a262ffad7e651de0c64", qop=auth, nc=0000003f, cnonce="b7e31fb393c93ca4"',
            'Connection': 'keep-alive',
            'Referer': 'http://11.8.0.67/',
            'Priority': 'u=0',
        }

        response = requests.get('http://11.8.0.67/cgi-bin/dlog.cgi', headers=headers)
        print(ip)
        print(response.json())


def read_ips_form_xls(file_path):
    df = pd.read_excel(file_path, 'Sheet1')

    # 将数据框转为二维数组（嵌套列表）
    data = df.values.tolist()
    check_ips = [row[1] for row in data if len(row) > 1]
    # 打印结果
    return check_ips


if __name__ == '__main__':
    doa_sn = read_ips_form_xls(luna_b_path)
    for sn in doa_sn:
        get_blog_by_ip(sn)
