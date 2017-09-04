# -*- coding: utf-8 -*-
import os, time, datetime, re


# 定义一个函数来找出发生变化的文件，给定两个时间，通过判断文件的修改时间来找
def change_file(base, time1_stamp, time2_stamp):
    # 建立两个空列表，用来装稍后找出的总文件和变更文件
    list_files = []
    list_change_file = []
    # 遍历输入的文件目录，并返回三个值的元祖，分别是每次遍历的路径、文件目录和文件名
    for root, dirs, files in os.walk(base):
        list_files.extend(list(files))
        # 遍历文件名列表
        for file in files:
            # 合成一个新路径
            f = os.path.join(root, file)
            # 获取该路径文件的最后修改时间
            mtime = os.path.getmtime(f)
            # 获取目标文件，目标文件的性质为后缀是'.js' '.erl' '.hrl'的文件，且最后修改时间介于输入的两个时间之间
            if os.path.splitext(f)[1] in ('.js', '.erl', '.hrl') and time1_stamp < mtime < time2_stamp:
                # 将目标文件加入上文中的列表中
                list_change_file.append(file)
    # 输出总文件列表和发生了改变的文件列表
    print('当前指定目录中的所有文件为：', list_files)
    print('发生了变更的文件有这些：', list_change_file)
    # 计算总文件数和发生变更的文件数
    num1 = len(list_files)
    num2 = len(list_change_file)
    # 计算变更率并输出
    change_rate = '变更度为：{:.2%}'.format(num2 / num1)
    print(change_rate)
    return change_rate

if __name__ == '__main__':
    while True:
        # 设置开始和退出
        Q = input('按任意键开始，按q退出！')
        if Q.lower() == 'q':
            exit()
        # 输入两个指定时间
        match1 = ''
        match2 = ''
        while not match1 or not match2:
            print('请严格按照格式输入！')
            time1 = input('请输入起始时间，格式为XXXX-XX-XX XX(24小时）:XX:XX: ')
            time2 = input('请输入结束时间，格式为XXXX-XX-XX XX(24小时）:XX:XX: ')
            match1 = re.match(r'^\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}:\d{2}$', time1)
            match2 = re.match(r'^\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}:\d{2}$', time2)
            continue
        # 将输入的时间格式化
        time1_list1 = time1.replace(' ', '-').replace(':', '-').split('-')
        time2_list1 = time2.replace(' ', '-').replace(':', '-').split('-')
        # 将格式化后的时间变成整型
        time1_list2 = map(int, time1_list1)
        time2_list2 = map(int, time2_list1)
        # 获取输入时间的datetime
        time1_str = datetime.datetime(*time1_list2)
        time2_str = datetime.datetime(*time2_list2)
        # 获取输入时间的时间戳
        time1_stamp = time.mktime(time1_str.timetuple())
        time2_stamp = time.mktime(time2_str.timetuple())
        # 输入想要计算的类型，例如int版本的客户端文件
        root_number = input('请输入目录名指定数字代号，int客户端为11，int服务端为12；patch客户端为21，\
patch服务端为22；release客户端为31，release服务端为32: ')
        while int(root_number) not in [11, 12, 21, 22, 31, 32]:
            root_number = input('请输入正确的数字代号： ')
            continue
        # 输入想要计算的模块文件夹名称
        key = input('请输入需要计算变更度的文件夹名称： ')
        root_dict = {'11': r'int\code\clientjs\game',
                     '12': r'int\code\server\p25',
                     '21': r'patch\code\clientjs\game',
                     '22': r'patch\code\server\p25',
                     '31': r'release\code\clientjs\game',
                     '32': r'release\code\server\p25'}
        while key not in os.listdir(root_dict[root_number]):
            key = input('请输入正确的文件夹名称： ')
            continue
        # 定义需要进入的文件夹目录
        base = os.path.join(root_dict[root_number], key)
        # 调用函数计算变更率
        change_file(base, time1_stamp, time2_stamp)
