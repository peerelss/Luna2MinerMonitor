import pandas as pd
from collections import Counter
import numpy as np

file_path = r'C:\Users\kevin\Documents\9月sn\盘点\9月份盘点统计.xls'
file_path2 = r'C:\Users\kevin\Documents\9月sn\盘点\snold.xls'

file_total = r'C:\Users\kevin\Documents\9月sn\total0909.xlsx'


# 读取Excel文件


def get_sn_from_excel(path):
    df = pd.read_excel(path)

    # 获取第三列的数据（假设第三列的索引是2，索引从0开始）
    third_column_data = df.iloc[:, 2].values

    # 将第三列数据转换为NumPy数组
    third_column_array = np.array(third_column_data)
    print(str(len(third_column_array)))
    return third_column_data


def get_sn_from_excel_by_sheet_name(name):
    df = pd.read_excel(file_total, sheet_name=name)

    # 获取第三列的数据（假设第三列的索引是2，索引从0开始）
    third_column_data = df.iloc[:, 2].values

    # 将第三列数据转换为NumPy数组
    third_column_array = np.array(third_column_data).tolist()
    return third_column_array


def get_all_sn(path, name):
    df = pd.read_excel(path, sheet_name=name)
    third_column_data = df.iloc[:, 0].values
    # 将第三列数据转换为NumPy数组
    third_column_array = np.array(third_column_data).tolist()
    return third_column_array


def get_emtpy():
    sn_a_send = get_sn_from_excel_by_sheet_name('总结一期送出')
    sn_a_get = get_sn_from_excel_by_sheet_name('总结一期接受')
    sn_b_send = get_sn_from_excel_by_sheet_name('总结二期送出')
    sn_b_get = get_sn_from_excel_by_sheet_name('总结二期接受')
    sn_all = (sn_a_get + sn_a_send + sn_b_send + sn_b_get)
    counter = Counter(sn_all)
    odd_count_strings = [string for string, count in counter.items() if count % 2 != 0]
    # 打印结果
    return odd_count_strings


def get_sn_1_from_h():
    df = pd.read_excel(r'C:\Users\kevin\Documents\9月sn\盘点\luna1formh.xls')
    third_column_data = df.iloc[:, 5].values
    # 将第三列数据转换为NumPy数组
    third_column_array = np.array(third_column_data).tolist()
    return third_column_array


def em():
    sn_1 = get_all_sn(
        r'C:\Users\kevin\Documents\WeChat Files\wxid_ulomi7v0bh8422\FileStorage\File\2024-08\TX—Luna矿场一期_0814_v6(1).xlsx',
        "SN反馈清单")[4:6268]
    sn_2 = get_all_sn(
        r'C:\Users\kevin\Documents\WeChat Files\wxid_ulomi7v0bh8422\FileStorage\File\2024-08\TX—Luna矿场二期_0814_v6(1).xlsx',
        "SN反馈清单")[4:5188]

    sn_a_send = get_sn_from_excel_by_sheet_name('总结一期送出')[660:]
    print(len(sn_a_send))
    sn_a_get = get_sn_from_excel_by_sheet_name('总结一期接受')[298:]
    print(len(sn_a_get))
    sn_b_send = get_sn_from_excel_by_sheet_name('总结二期送出')[261:]
    print(len(sn_b_send))
    sn_b_get = get_sn_from_excel_by_sheet_name('总结二期接受')[148:]
    print(len(sn_b_get))
    sn_a_out = sn_1[-365:]
    print(len(sn_a_out))
    sn_all = sn_a_out + sn_a_send
    for sn in sn_all:
        if sn not in sn_a_get:
            print(sn)

def offline_list():
    with open(r'C:\Users\kevin\Documents\9月sn\下架.txt', 'r') as file:
        # 使用 readlines() 读取每一行，并去除换行符
        lines = [line.strip() for line in file.readlines()]

    return lines

def get_luna_a():
    offline_list1=offline_list()
    path_luna2 = r'C:\Users\kevin\Documents\9月sn\盘点\luna10911.xlsx'
    for i in  range(1,12):
        sn_1 = pd.read_excel(path_luna2, sheet_name=i).values.tolist()
        result_list=[]
        for sn in sn_1:
            if len(str(sn[2]))>5:
                result_list.append(sn[2])
                print(sn[2])
        #print(len(result_list))
def e():
    sn_a_send = get_sn_from_excel_by_sheet_name('总结一期送出')
    print(len(sn_a_send))
    sn_a_get = get_sn_from_excel_by_sheet_name('总结一期接受')
    print(len(sn_a_get))
    sn_b_send = get_sn_from_excel_by_sheet_name('总结二期送出')
    print(len(sn_b_send))
    sn_b_get = get_sn_from_excel_by_sheet_name('总结二期接受')
    print(len(sn_b_get))
    sn_all = (sn_a_get + sn_a_send + sn_b_send + sn_b_get)
    counter = Counter(sn_all)
    odd_count_strings = [string for string, count in counter.items() if count % 2 != 0]
    # 打印结果
    print(len(odd_count_strings))
    for odd in odd_count_strings:
        print(odd)

if __name__ == "__main__":
    get_luna_a()
