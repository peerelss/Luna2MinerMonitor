import pandas as pd

file_sn_luna_a = r'C:\Users\MSI\Documents\luna\TX-Luna矿场一期盘点1107v2(2).xlsx'
file_sn_luna_b = r'C:\Users\MSI\Documents\luna\TX-Luna矿场二期盘点1107v2(2).xlsx'
file_check_luna_a = r'C:\Users\MSI\Documents\luna\10. Luna Squares Texas LLC (LSTX01)-100台.xlsx'
file_check_luna_b = r'C:\Users\MSI\Documents\luna\14. Luna Squares Texas LLC (LSTX02)-共5184台抽检100台.xlsx'
from openpyxl import Workbook


def get_miner_luna_a():
    file_p_luna_a = r'C:\Users\MSI\Downloads\一期比特大陆s19xp型号IP和SN统计.xlsx'
    box_list = ['1号厂房', '2号厂房', '3号厂房', "4号厂房", '5号厂房', '6号厂房', '7号厂房', '8号厂房', '9号厂房',
                '10号厂房']
    total_sn_list_a = []
    for box in box_list:
        box_sn = get_miner_detail_by_file_and_name(file_p_luna_a, box)
        total_sn_list_a = total_sn_list_a + box_sn
    return total_sn_list_a


def get_miner_luna_b():
    file_p_luna_a = r'C:\Users\MSI\Downloads\二期比特大陆s19xp型号IP和SN统计.xlsx'
    box_list = ['1号厂房', "4号厂房", '5号厂房', '6号厂房', '7号厂房', '8号厂房', '9号厂房', '10号厂房', '11号厂房',
                '12号厂房', '13号厂房', '14号厂房', '15号厂房']
    total_sn_list_b = []
    for box in box_list:
        box_sn = get_miner_detail_by_file_and_name(file_p_luna_a, box)
        total_sn_list_b = total_sn_list_b + box_sn
    return total_sn_list_b


def write_sn_to_excel(list_sn):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # 将二维数组写入工作表
    for row in list_sn:
        ws.append(row)

    # 保存为 Excel 文件
    file_path = "example2.xlsx"
    wb.save(file_path)

    print(f"数据已成功保存到 {file_path}")


def get_miner_detail_by_file_and_name(file_path_sn, sheet_name):
    df = pd.read_excel(file_path_sn, sheet_name)

    # 将数据框转为二维数组（嵌套列表）
    data = df.values.tolist()

    # 打印结果
    return data


def get_sn_by_ip(ip):
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Authorization': 'Digest username=root, realm=antMiner Configuration, nonce=93fc6325b206c6fa28f7387b59618687, uri=/cgi-bin/get_system_info.cgi, response=26d3c31d81d52a9b267a3f8b6657b60a, qop=auth, nc=00000034, cnonce=60d54b0dedd9439a',
        'Connection': 'keep-alive',
        'Referer': 'http://11.12.2.95/',
    }

    response = requests.get('http://11.12.2.95/cgi-bin/get_system_info.cgi', headers=headers)

    return response.json()['serinum']


if __name__ == '__main__':
    list_luna_check_a = get_miner_detail_by_file_and_name(file_check_luna_a, 'Sheet1')
    list_luna_check_b = get_miner_detail_by_file_and_name(file_check_luna_b, 'Sheet1')
    check_sn_list_a = [row[0] for row in list_luna_check_a if len(row) > 0]
    # check_sn_list_b = [row[4] for row in list_luna_check_b if len(row) > 4]
    # print(check_sn_list_a)
    # for sn_a in list_luna_sn_a:
    #    if sn_a[1] in check_sn_list_a:
    #        print(sn_a)
    total_sn_list_luna_b = get_miner_luna_b()
    result_sn_location = []
    for t in total_sn_list_luna_b:
        if t[2] in check_sn_list_a:
            result_sn_location.append(t)
    write_sn_to_excel(result_sn_location)
