# -*- coding: utf-8 -*-
"""通过文件最后修改时间计算指定时间内模块文件夹中文件的变化率"""
__author__ = 'Huang Lun'
import time
import datetime
import os
import re
from xlrd import open_workbook
from xlutils.copy import copy


def input_start_time():
    """获取起始的输入时间"""
    time_start = input('请输入起始时间，格式为XXXX-XX-XX，可留空: ')
    if time_start:
        match = re.match(r'^\d{4}-\d{2}-\d{2}$', time_start)
        if not match:
            return input_start_time()
        else:
            # 获取指定时间的时间戳
            time_array = time.strptime(time_start, '%Y-%m-%d')
            time_stamp = int(time.mktime(time_array))
            print('起始时间为: ', end='')
            print(time.strftime('%Y-%m-%d', time_array))
    else:
        # 获取七天前的时间元组和时间戳
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        time_stamp = int(time.mktime(seven_days_ago.timetuple()))
        print('起始时间为: ', end='')
        print(seven_days_ago)
    return time_stamp


def input_end_time():
    """获取结束的输入时间"""
    time_end = input('请输入结束时间，格式为XXXX-XX-XX，可留空: ')
    if time_end:
        match = re.match(r'^\d{4}-\d{2}-\d{2}$', time_end)
        if not match:
            return input_end_time()
        else:
            # 获取给定时间的时间戳
            time_array = time.strptime(time_end, '%Y-%m-%d')
            time_stamp = int(time.mktime(time_array))
            print('结束时间为: ', end='')
            print(time.strftime('%Y-%m-%d', time_array))
    else:
        # 获取现在的时间戳
        time_stamp = int(time.time())
        print('结束时间为: ', end='')
        print(datetime.datetime.now())
    return time_stamp


def save_to_file(module_name, module_root, time1_stamp, time2_stamp):
    """将每个模块的结果写入excel文件"""
    # 计算总文件数和总变更文件数
    total_files_num = 0
    total_changed_files_num = 0
    rexcel = open_workbook('版本变更度.xls')  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
    row = rows

    # 判断路径是否是文件夹，如果是则遍历计算结果
    if os.path.isdir(module_root):
        files_num, changed_files_num, change_rate = traverse_and_calculate(time1_stamp, time2_stamp, module_root)
        total_files_num += files_num
        total_changed_files_num += changed_files_num
        if str(change_rate) != '0.00%':
            table.write(row, module_name, change_rate)

    return total_files_num, total_changed_files_num


def run(root_dict, version, time1_stamp, time2_stamp):
    """总函数得到版本变更度结果文件"""
    # 获得客户端和服务端的所有模块文件夹
    client_modules_list = os.listdir(root_dict[version][0])
    server_modules_list = os.listdir(root_dict[version][1])

    # 创建一个文本文件，将最终结果写入文件
    file_name = version + '-changed-rate.txt'
    total_files_num = 0
    total_changed_files_num = 0

    # 遍历所有的客户端模块
    with open(file_name, 'a') as f:
        f.write('当前版本中客户端的变更模块有：\n')
    for client_module in client_modules_list:
        client_module_root = os.path.join(root_dict[version][0], client_module)

        # 得到客户端中的文件总数和变化的文件总数，并加到最终的数据中
        total_client_files_num, total_client_changed_files_num = save_to_file(
            file_name, client_module, client_module_root, time1_stamp, time2_stamp)
        total_files_num += total_client_files_num
        total_changed_files_num += total_client_changed_files_num

    # 遍历所有的服务端模块
    with open(file_name, 'a') as f:
        f.write('\n当前版本中服务端的变更模块有：\n')
    for server_module in server_modules_list:
        server_module_root = os.path.join(root_dict[version][-1], server_module)

        # 得到服务端中的文件总数和变化的文件总数，并加到最终的数据中
        total_server_files_num, total_server_changed_files_num = save_to_file(
            file_name, server_module, server_module_root, time1_stamp, time2_stamp)
        total_files_num += total_server_files_num
        total_changed_files_num += total_server_changed_files_num

    # 计算总变更度并保存到文件中
    total_change_rate = '{:.2%}'.format(total_changed_files_num / total_files_num)
    with open(file_name, 'a') as f:
        f.write('\n当前版本的总变更度为: ' + str(total_change_rate))


def traverse_and_calculate(time1_stamp, time2_stamp, module_root):
    """遍历单个模块文件夹并计算结果"""
    # 建立两个个列表存储总文件和发生变更的文件
    files_list = []
    changed_files_list = []

    # 遍历模块目录
    for root, dirs, files in os.walk(module_root):
        # 遍历文件列表，并将文件加入到上文列表中
        for file in files:
            files_list.append(file)

            # 合成一个新路径
            file_root = os.path.join(root, file)

            # 获取该路径文件的最后修改时间
            mtime = os.path.getmtime(file_root)

            # 获取目标文件，目标文件的性质为后缀是'.js' '.erl' '.hrl'的文件，且最后修改时间介于输入的两个时间之间
            if os.path.splitext(file_root)[1] in ('.js', '.erl', '.hrl') and time1_stamp < mtime < time2_stamp:
                # 将目标文件加入上文中的列表中
                changed_files_list.append(file)

    # 计算该模块下文件数和发生变更的文件数
    num1 = len(files_list)
    num2 = len(changed_files_list)

    # 计算变更率
    change_rate = '{:.2%}'.format(num2 / num1)

    return num1, num2, change_rate


def save_excel(client_modules_list, server_modules_list):
    """将结果写入excel"""
    rexcel = open_workbook('版本变更度.xls')  # 用wlrd提供的方法读取一个excel文件
    rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet


if __name__ == '__main__':
    root_dict = {'int': [r'int\code\clientjs\game', r'int\code\server\p25'],
                 'patch': [r'patch\code\clientjs\game', r'patch\code\server\p25'],
                 'release': [r'release\code\clientjs\game', r'release\code\server\p25']
                 }
    while True:
        # 设置开始和退出
        q = input('按任意键开始，按q退出！')
        if q.lower() == 'q':
            exit()

        # 输入两个指定时间
        time1_stamp = input_start_time()
        time2_stamp = input_end_time()

        # 输入版本类型
        version = ''
        while version not in ['int', 'patch', 'release']:
            version = input('请输入版本类型（int、patch、release）： ')
            continue

        # 运行函数
        run(root_dict, version, time1_stamp, time2_stamp)