import requests

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
ip_range = [0, 1, 2, 3 ]
ip_3 = [1, 2, 3, 6, 7, 8]


def get_miner_mode(ip):
    print(ip)
    try:
        response = requests.get('http://' + ip + '/cgi-bin/stats.cgi', headers=headers, verify=False)
        print(response.json()['STATS'][0]['miner-mode'])
    except:
        pass


if __name__ == "__main__":
    for ip1 in container_range:
        for ip2 in ip_range:
            for ip3 in ip_3:
                get_miner_mode("10." + str(ip1) + '.' + str(ip2) + '.' + str(ip3))
