# -*- coding: utf-8 -*-
"""通过文件最后修改时间计算指定时间内模块文件夹中文件的变化率"""
__author__ = 'Huang Lun'
import time
import datetime
import os
import re


def traversal_folders(version, module_name, time1, time2, root_dict):
    """如果模块文件名服务器和客户端都有的时候处理方式"""
    module_folder_roots = join_module_name_root(version, module_name, root_dict)
    total_files_list, total_change_files_list = [], []
    for module_name_root in module_folder_roots:
        file_tuple = traversal_folder(module_name_root, time1, time2)
        total_files_list += file_tuple[0]
        total_change_files_list += file_tuple[1]

    # 将计算结果写入文件保存
    save_to_file(version, total_files_list, total_change_files_list)


def traversal_folder(version, time1, time2):
    """遍历需要计算的模块文件夹"""
    # 获取时间段
    time1_stamp = time1_assigned(time1)
    time2_stamp = time2_assigned(time2)

    # 建立四个列表，用来装总模块、总文件和稍后找出的变更模块以及变更文件
    modules_list = os.listdir(version)
    files_list = []
    change_modules_list = []
    change_files_list = []

    # 遍历输入的文件目录，并返回三个值的元祖，分别是每次遍历的路径、文件目录和文件名
    for root, dirs, files in os.walk(version):
        # 遍历文件名列表
        for file in files:
            files_list.append(file)

            # 合成一个新路径
            f = os.path.join(root, file)

            # 获取该路径文件的最后修改时间
            mtime = os.path.getmtime(f)

            # 获取目标文件，目标文件的性质为后缀是'.js' '.erl' '.hrl'的文件，且最后修改时间介于输入的两个时间之间
            if os.path.splitext(f)[1] in ('.js', '.erl', '.hrl') and time1_stamp < mtime < time2_stamp:
                # 将目标文件加入上文中的列表中
                change_files_list.append(file)
    return files_list, change_files_list


def save_to_file(version, total_files_list, total_change_files_list):
    """将计算结果写入文件保存"""
    # 计算总文件数和发生变更的文件数
    num1 = len(total_files_list)
    num2 = len(total_change_files_list)

    # 计算变更率并输出
    change_rate = '{:.2%}'.format(num2 / num1)
    print(change_rate)

    # 保存到文件
    file_name = version + '-changed-rate.txt'
    with open(file_name, 'w') as f:
        f.write('当前模块下所有文件为:\n')
        for file in total_files_list:
            f.write(file + '\n')
        f.write('\n\n发生了变更的文件有这些:\n')
        for change_file in total_change_files_list:
            f.write(change_file + '\n')
        f.write('\n\n当前版本变更度为: ' + str(change_rate) + '\n\n')


def time1_assigned(time1):
    """指定需要查询的起始时间，若不设置则默认现在往前一个星期时间"""
    if not time1:
        # 获取七天前的时间元组和时间戳
        seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7))
        time1_stamp = int(time.mktime(seven_days_ago.timetuple()))
    else:
        # 获取指定时间的时间戳
        time1_array = time.strptime(time1, '%Y-%m-%d')
        time1_stamp = int(time.mktime(time1_array))
    return time1_stamp


def time2_assigned(time2):
    """指定需要查询的结束时间，若不设置则默认现在的时间"""
    if not time2:
        # 获取现在的时间戳
        time2_stamp = int(time.time())
    else:
        # 获取给定时间的时间戳
        time2_array = time.strptime(time2, '%Y-%m-%d')
        time2_stamp = int(time.mktime(time2_array))
    return time2_stamp


def join_module_name_root(version, module_name, root_dict):
    """将模块名和版本目录拼接成最终路径"""
    module_folder_roots = []
    for module_root in root_dict[version]:
        module_folder_root = os.path.join(module_root, module_name)
        if os.path.exists(module_folder_root):
            module_folder_roots.append(module_folder_root)
    return module_folder_roots


def input_time():
    """获取输入时间"""
    time = input('请输入时间，格式为XXXX-XX-XX，也可以留空: ')
    if not time:
        return time
    else:
        match = re.match(r'^\d{4}-\d{2}-\d{2}$', time)
        while not match:
            return input_time()


def verify_module_name(root_dict):
    """验证模块名是否正确"""
    module_list = []
    for module_roots in root_dict.values():
        for module_root in module_roots:
            module_list += os.listdir(module_root)
    return module_list


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
        version = ''
        module_name = ''
        module_list = verify_module_name(root_dict)
        print('起始时间')
        time1 = input_time()
        print('结束时间')
        time2 = input_time()

        # 输入版本类型
        while version not in ['int', 'patch', 'release']:
            version = input('请输入版本类型（int、patch、release）： ')
            continue

        # 输入模块名
        while module_name not in module_list:
            module_name = input('请输入模块文件名： ')
            continue

        # 调用函数
        traversal_folders(version, module_name, time1, time2, root_dict)
