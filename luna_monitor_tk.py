import tkinter as tk
from datetime import datetime
import random


def update_time_label():
    """更新最后更新时间"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_label.config(text=f"最后更新时间: {current_time}")


def update_status(box_id, is_normal):
    """
    更新矿箱状态。
    参数:
        box_id (int): 矿箱编号 (1-10)。
        is_normal (bool): True 表示正常，False 表示不正常。
    返回:
        bool: 状态值。
    """
    if box_id < 1 or box_id > 10:
        print(f"错误: 矿箱编号 {box_id} 无效！")
        return False  # 编号超出范围

    status_label = buttons[box_id - 1]  # 获取对应的矿箱状态组件
    if is_normal:
        status_label.config(bg="green", text=f"{box_id}\n正常")
        return True
    else:
        status_label.config(bg="red", text=f"{box_id}\n不正常")
        return False


def random_update():
    """随机更新矿箱状态"""
    for i in range(1, 11):  # 遍历所有矿箱编号
        is_normal = random.choice([True, False])  # 随机生成状态
        update_status(i, is_normal)  # 更新每个矿箱的状态
    update_time_label()  # 更新时间显示


def create_gui():
    """创建主界面"""
    global root, buttons, time_label

    # 创建主窗口
    root = tk.Tk()
    root.title("矿箱状态监控")
    root.geometry("600x450")
    root.resizable(False, False)

    # 主框架
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True, fill=tk.BOTH, pady=10)

    # 状态按钮列表
    buttons = []
    for i in range(10):
        frame = tk.Frame(main_frame, bg="white", padx=5, pady=5)
        frame.grid(row=i // 5, column=i % 5, padx=10, pady=10)

        # 圆角背景的标签
        label = tk.Label(
            frame,
            text=f"{i + 1}\n正常",  # 默认显示正常状态
            bg="green",  # 初始背景色为绿色
            fg="black",  # 字体颜色为黑色
            font=("Arial", 12, "bold"),  # 字体样式
            width=6,  # 标签宽度
            height=3,  # 标签高度
            relief="ridge",  # 边框样式
            justify="center"  # 文本居中
        )
        label.pack()
        buttons.append(label)

    # 最后更新时间标签
    time_label = tk.Label(root, text="", font=("Arial", 12), fg="black", bg="white")
    time_label.pack(pady=10)
    update_time_label()  # 初始化时间

    # 更新状态按钮
    update_button = tk.Button(
        root,
        text="更新状态",
        font=("Arial", 12, "bold"),
        bg="blue",
        fg="white",
        command=random_update  # 按钮点击时调用 random_update 函数
    )
    update_button.pack(pady=10)


if __name__ == '__main__':
    create_gui()

    # 启动 Tkinter 主循环
    root.mainloop()
