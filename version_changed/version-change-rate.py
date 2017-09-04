# -*- coding: utf-8 -*-
"""通过文件最后修改时间计算指定时间内模块文件夹中文件的变化率"""
__author__ = 'Huang Lun'
import time
import datetime
import os
import re


def traversal_folder(module_root, time1, time2):
    """遍历单个模块文件夹并计算其变更度"""
    # 获取时间段
    time1_stamp = time1_assigned(time1)
    time2_stamp = time2_assigned(time2)

    # 建立两个个列表存储总文件和发生变更的文件
    files_list = []
    changed_files_list = []

    # 遍历模块目录，并返回三个值的元祖，分别是每次遍历的路径、文件目录和文件名
    for root, dirs, files in os.walk(module_root):
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
                changed_files_list.append(file)

    # 计算总文件数和发生变更的文件数
    num1 = len(files_list)
    num2 = len(changed_files_list)

    # 计算变更率
    change_rate = '{:.2%}'.format(num2 / num1)

    return change_rate, files_list, changed_files_list


def traversal_and_save(modeles_list, root_dict, version, time1, time2):
    """遍历模块并存储文件"""
    # 建立两个空列表装总文件和总变更文件，一个空字典装结果
    total_files_list = []
    total_changed_files_list = []
    results = {}
    for module_name in modeles_list:
        module_root = os.path.join(root_dict[version][0], module_name)
        if os.path.isdir(module_root):
            change_rate = traversal_folder(module_root, time1, time2)[0]
            total_files_list += traversal_folder(module_root, time1, time2)[1]
            total_changed_files_list += traversal_folder(module_root, time1, time2)[-1]
            results[module_name] = change_rate
    return total_files_list, total_changed_files_list, results


def save_file(change_rate, version, module_name):
    """将计算结果保存到文件中"""
    file_name = version + '-changed-rate.txt'
    with open(file_name, 'a') as f:
        f.write(module_name + ' ----- ' + str(change_rate) + '\n')


def traversal_total_folders(root_dict, version, time1, time2):
    """遍历服务端和客户端中每个模块文件夹并存储结果"""
    # 分别遍历服务端和客户端，并得到总文件和总变更文件
    client_modules_list = os.listdir(root_dict[version][0])
    server_modules_list = os.listdir(root_dict[version][1])
    client_files_list, changed_client_files_list = traversal_and_save(client_modules_list,
                                                                      root_dict, version, time1, time2)
    server_files_list, changed_server_files_list = traversal_and_save(server_modules_list,
                                                                      root_dict, version, time1, time2)
    total_files_list = client_files_list + server_files_list
    total_changed_files_list = changed_client_files_list + changed_server_files_list

    # 计算总变更度并保存到文件中
    file_name = version + '-changed-rate.txt'
    total_files_num = len(total_files_list)
    total_changed_files_num = len(total_changed_files_list)
    total_change_rate = '{:.2%}'.format(total_changed_files_num / total_files_num)
    with open(file_name, 'a') as f:
        f.write('\n当前版本的总变更度为 ---- ' + str(total_change_rate))


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


def input_time():
    """获取输入时间"""
    time = input('请输入时间，格式为XXXX-XX-XX（起始时间留空默认为一星期前，结束时间留空默认为今天）: ')
    if not time:
        return time
    else:
        match = re.match(r'^\d{4}-\d{2}-\d{2}$', time)
        while not match:
            return input_time()


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
        print('起始时间')
        time1 = input_time()
        print('结束时间')
        time2 = input_time()

        # 输入版本类型
        version = ''
        while version not in ['int', 'patch', 'release']:
            version = input('请输入版本类型（int、patch、release）： ')
            continue

        # 调用函数
        traversal_total_folders(root_dict, version, time1, time2)
