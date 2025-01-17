import pandas as pd
import os
import requests

# 文件路径和 Sheet 名称
input_file_path = r'C:\Users\MSI\Downloads\一期比特大陆s19xp型号IP和SN统计(1).xlsx'  # 替换为你的文件路径
input_file_path_luna2 = r'C:\Users\MSI\Downloads\二期比特大陆s19xp型号IP和SN统计(9).xlsx'
sheet_names_xp = ['4号厂房', '5号厂房', '6号厂房', '7号厂房', '11号厂房', '12号厂房', '13号厂房', '14号厂房',
                  '15号厂房']
sheet_names_s21 = ['1号厂房', '8号厂房', '9号厂房', '10号厂房']
sheet_names = ['1号厂房', '2号厂房', '3号厂房', '4号厂房', '5号厂房', '6号厂房', '7号厂房', '8号厂房', '9号厂房',
               '10号厂房']
output_file_path = 'filtered_B_C_column_all_luna_a.xlsx'  # 替换为你的输出文件路径


def get_ip_sn_from_xlsx(xlsx_file, sheet_name_sn):
    try:
        for sheet_name in sheet_name_sn:
            # 读取指定的 Sheet
            data = pd.read_excel(xlsx_file, sheet_name=sheet_name)

            # 转换为二维数组
            array = data.fillna(0).values.tolist()
            for array_sn in array:
                if len(str(array_sn[1])) > 7 and len(str(array_sn[2])) >= 10:
                    is_sn_correct(array_sn[1], array_sn[2])

    except FileNotFoundError:
        print(f"输入文件 {xlsx_file} 不存在。")
    except IndexError:
        print(f"Sheet 中没有足够的列（至少需要 3 列）。")
    except ValueError as e:
        print(f"读取 Sheet 时出错：{e}")
    except Exception as e:
        print(f"其他错误：{e}")


def get_sn_by_ip(ip):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="057670ab3b300adea04daf0396ae793a", uri="/cgi-bin/get_system_info.cgi", response="c7f764c783f3f81d1def4a7876dd7287", qop=auth, nc=00000045, cnonce="2b40a932315aab1e"',
            'Connection': 'keep-alive',
            'Referer': 'http://10.7.0.4/',
        }

        response = requests.get('http://' + ip + '/cgi-bin/get_system_info.cgi', headers=headers)
        return response.json()['serinum']
    except Exception as e:
        print(f"{ip} 其他错误：{e}")
        return 'unknown'


def is_sn_correct(ip, sn):
    sn_from_ip = get_sn_by_ip(ip.strip())
    # print(f"ip: {ip},sn:{sn},sn_form_ip:{sn_from_ip}")
    if len(sn_from_ip) != 17 or sn[-4:] != sn_from_ip[-4:]:
        print(f"ip: {ip},sn:{sn},sn_form_ip:{sn_from_ip}")


def set_miner_ip_to_dhcp():
    pass



if __name__ == '__main__':
    get_ip_sn_from_xlsx(input_file_path_luna2, sheet_names_s21)
