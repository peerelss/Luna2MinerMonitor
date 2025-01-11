import pandas as pd
import os

# 文件路径和 Sheet 名称
input_file_path= r'C:\Users\MSI\Downloads\一期比特大陆s19xp型号IP和SN统计(1).xlsx'  # 替换为你的文件路径
input_file_path_luna1  = r'C:\Users\MSI\Downloads\二期比特大陆s19xp型号IP和SN统计(8).xlsx'
sheet_names_xp = ['4号厂房', '5号厂房', '6号厂房', '7号厂房', '11号厂房', '12号厂房', '13号厂房', '14号厂房',
               '15号厂房']
sheet_names_s21 = ['1号厂房', '8号厂房', '9号厂房', '10号厂房']
sheet_names = ['1号厂房', '2号厂房', '3号厂房','4号厂房', '5号厂房', '6号厂房', '7号厂房', '8号厂房', '9号厂房', '10号厂房']
output_file_path = 'filtered_B_C_column_all_luna_a.xlsx'  # 替换为你的输出文件路径
all_filtered_data = pd.DataFrame()

try:
    for sheet_name in sheet_names:
        # 读取指定的 Sheet
        data = pd.read_excel(input_file_path, sheet_name=sheet_name)

        # 筛选 C 列（第三列）不为空的值
        filtered_data = data[data.iloc[:, 2].notna()]  # 第三列不为空的行
        c_column_only = filtered_data.iloc[:, [1,2]]  # 仅保留第三列

        # 将结果追加到累积 DataFrame
        all_filtered_data = pd.concat([all_filtered_data, c_column_only], ignore_index=True)

    # 写入最终结果到 Excel 文件
    if os.path.exists(output_file_path):
        # 如果文件已存在，追加模式写入
        with pd.ExcelWriter(output_file_path, engine='openpyxl', mode='a') as writer:
            all_filtered_data.to_excel(writer, index=False, header=False)
    else:
        # 如果文件不存在，创建新文件
        all_filtered_data.to_excel(output_file_path, index=False, header=True)

    print(f"所有 Sheet 的第 C 列不为空的值已写入文件：{output_file_path}")
except FileNotFoundError:
    print(f"输入文件 {input_file_path} 不存在。")
except IndexError:
    print(f"Sheet 中没有足够的列（至少需要 3 列）。")
except ValueError as e:
    print(f"读取 Sheet 时出错：{e}")
except Exception as e:
    print(f"其他错误：{e}")


def ip_to_location(ip: str) -> str:
    """
    将矿机 IP 地址转换为厂房中架子上的实际位置。

    参数:
        ip (str): 矿机 IP 地址，例如 "192.168.4.30"

    返回:
        str: 实际位置描述，例如 "厂房 4 架子 21 第 6 行第 5 列"
    """
    try:
        # 拆分 IP 地址并提取有用部分
        ip_parts = ip.split('.')
        if len(ip_parts) != 4:
            return "无效的 IP 格式"

        # 提取厂房编号 (第二段) 和矿机位置 (第三段和第四段)
        factory_id = int(ip_parts[1])  # 厂房编号
        rack_range = int(ip_parts[2])  # 架子分段（0-4）
        machine_id = int(ip_parts[3])  # 架子内矿机编号（1-150）

        # 验证范围
        if not (1 <= factory_id <= 4):
            return "厂房编号超出范围"
        if not (0 <= rack_range <= 4):
            return "架子范围编号超出范围"
        if not (1 <= machine_id <= 150):
            return "矿机编号超出范围"

        # 计算架子编号
        rack_id = rack_range * 5 + (machine_id - 1) // 30 + 1

        # 计算在架子上的行和列
        position_within_rack = (machine_id - 1) % 30
        row = position_within_rack // 5 + 1
        col = position_within_rack % 5 + 1

        # 返回实际位置
        return f"厂房 {factory_id} 架子 {rack_id} 第 {row} 行第 {col} 列"

    except ValueError:
        return "IP 地址解析失败，请确保格式正确且所有段均为整数"


# 示例测试
ip_example = "192.4.3.120"
location = ip_to_location(ip_example)
print(location)
