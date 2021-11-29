# coding=utf-8
import datetime
import time
import os
import subprocess
import xlrd
import pickle
# from datetime import datetime
import datetime
from generate_path_csv import *


def read_pickle_num(temp_file_name, temp_num=0, MAX_NUM_PATHS=0, over_write_flag=False, over_write_value=0):
    # content = temp_num #如果该文件不存在，则加载默认值
    content = 1  # 初始值
    # MAX_NUM_PATHS = MAX_NUM_PATHS
    if over_write_flag:
        # 默认为False，不强制重写采集某条记录，设置为True时，则强制重写采集第over_write_value记录。
        content = over_write_value
    else:
        if temp_num == 0:
            # 不复位，读取暂存值
            if os.path.exists(temp_file_name):
                f = open(temp_file_name, 'rb')
                content = pickle.load(f)
                f.close()
            # 如果达到最大值，则置1
            if content == MAX_NUM_PATHS:
                content = 1
        # else:
        #     os.remove(temp_file_name)
        #     content = 1  # 初始值
        #     # global num_temp
        #     # temp_num = 0
    return content


def run_each_path(action_sequence):
    flag = True
    action_cnt = 0
    click_time_sequences = []
    for each_action in action_sequence[1:]:
        # 输入0表示成功，其他为故障
        click_ok = input("请点击【" + each_action + "】-------“直接按回车表示成功，其他任意键+回车表示失败”")
        if click_ok == '':
            # print("此动作采集成功!",each_action)
            this_action_time = "act-" + str(action_cnt) + "--" + str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            click_time_sequences.append(this_action_time)
            print(this_action_time, " OK!")
            action_cnt += 1
        else:
            # 该动作没有成功，则停止采集。
            print("错误数据，则停止采集！")
            flag = False
            break
    return flag, click_time_sequences


def write_click_time_sequences(file_path, click_time_sequences):
    # 把记录内容写到目标文件中
    with open(file_path, 'w') as fobj:
        for item in click_time_sequences:
            fobj.write(item + '\n')
    # fobj.close()


def check_overwrite(file_name):
    # 检测每条路径是否重写时的应答
    Flag = True
    while Flag:
        input_str = input(file_name + "--该文件已经存在，是否覆盖(y/n)")
        if input_str == 'y' or input_str == 'n':
            # Flag = False
            return input_str
        else:
            print("只能输入y/n,其他内容无效")


def check_runing(num):
    # 检测每条路径是否重写时的应答
    Flag = True
    while Flag:
        input_str = input("下一条路径num【" + str(num) + "】是否执行(num值/other)")
        # print("检测到的内容：",type(input_str))
        if input_str == str(num):
            Flag = True
            return Flag
        else:
            print("只能输入num值表示执行新的路径，other表示暂时")


def start_collect_traffic(traffic_path, network_card):
    try:
        order = r'tshark -i ' + network_card + ' -p -n -w  %s"' % traffic_path
        # order = 'adb shell su -c "/data/local/tcpdump port 80 or 443 -i any -p -n -s 0 -w /sdcard/%s.pcap"' % f
        subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    except Exception as e:
        print("运行错误类型1：", e)


def stop_collect_taffic():
    try:
        order = 'taskkill /F /IM tshark.exe /t'
        subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    except Exception as e:
        print("运行错误类型2：", e)


def control_path_step(all_paths, num, max_num, student_name="zhangsan", batch='2021_11_1', Applet_name='None',
                      network_card='WLAN', one_sequence_len=5):
    # print(len(all_paths))
    # student_name = student_name +  '_' + str(cycles_time) +'_'+ datetime.datetime.now().strftime("%Y-%m-%d")  # 新文件名
    student_name_path = student_name + '_' + Applet_name + '_' + str(batch)  # 新文件名
    path = "D:\\" + student_name + "\\" + student_name_path
    if not os.path.isdir(path):
        os.makedirs(path)
        num_temp = 1  # 采集序号num的复位标志，1表示为复位归零，从新开始计算值，0表示使用采集中间暂存值，不用从新计数，正常批量采集时都是默认值0,新的小程序第一次采集时，都复位
        num = read_pickle_num(this_Applet_name + '_temp_num.bat', num_temp, MAX_NUM_PATHS=max_num,
                              over_write_flag=False,
                              over_write_value=1)  # 中间暂停时的记录值，当某条记录错误，手动强制则从新采集第over_write_value条，
    else:
        if len(os.listdir(path + "\\click")) == 0:
            num = 1  # 强制复位。
    leftdown_num = 0
    result = ""
    show_boolen = True
    # num =26  # 采集路径编号
    MAX_NUM_PATHS = max_num  # 单个采集者，本批次需要采集路径（记录）总条数
    while num <= MAX_NUM_PATHS:
        if num > one_sequence_len:
            this_all_paths_index = divmod(num, one_sequence_len)[1]
            this_all_paths_index = this_all_paths_index - 1
        else:
            this_all_paths_index = num - 1
        try:
            if check_runing(num):
                common_file_name = Applet_name + "_" + str(batch) + "_" + str(num)  # txt与pcap共用的文件名字
                action_sequence_file_name = common_file_name + ".txt"
                if not os.path.isdir(path + "\\click"):
                    os.makedirs(path + "\\click")  # 生成click文件夹
                action_sequence_file_path = os.path.join(path + "\\click", action_sequence_file_name)  # 存储动作名称的路径
                if os.path.exists(action_sequence_file_path):
                    # 存在该文件
                    input_str = check_overwrite(action_sequence_file_name)
                    # print(input_str)
                    if input_str == "y":
                        print("……" * 10, "路径【" + str(num) + "】")
                        print("覆盖", all_paths[this_all_paths_index])
                        action_sequence = all_paths[this_all_paths_index]
                        traffic_file_name = common_file_name + ".pcap"
                        if not os.path.isdir(path + "\\traffic"):
                            os.makedirs(path + "\\traffic")
                        traffic_path = os.path.join(path + "\\traffic", traffic_file_name)
                        start_collect_traffic(traffic_path, network_card)
                        time.sleep(2)  # 强制控制睡眠时间,等待tshark 正常启动
                        back_flag, click_time_sequences = run_each_path(action_sequence)
                        if back_flag:
                            # 该路径成功采集
                            print("-.-" * 10, "路径采集成功！请稍微，数据存储后按提示进行下一条路径操作")
                            num += 1  # 覆盖成功后，再增加路径数值
                            time.sleep(3)  # 强制控制睡眠时间,把关闭动作的流量采集完毕
                            stop_collect_taffic()
                            write_click_time_sequences(action_sequence_file_path,
                                                       click_time_sequences)  # 把点击时间序列写入到txt文档中
                        else:
                            print("该路径没有成功采集，退回重新采集")
                            # num = num - 1 #num值不变，继续执行
                    else:
                        # file_name = Applet_name+"_" + str(num) + ".txt"
                        # file_path = os.path.join(path, file_name)
                        print("-" * 30, "已经过采集的路径【" + str(num) + "】", "-" * 30)
                        print("不覆盖,继续采集,当前为", action_sequence_file_path,
                              all_paths[this_all_paths_index][0])  # 则跳过已经存在的数值
                        num += 1  # 不覆盖，则增加路径数值，直接进入一次采集
                else:
                    # num += 1
                    # 不在已经存在的文件
                    # file_name = Applet_name+"_" + str(batch) + "_" + str(num) + ".txt"
                    # file_path = os.path.join(path + "\\click", file_name)
                    print("*" * 30, "路径【" + str(num) + "】", "*" * 30)
                    traffic_file_name = common_file_name + ".pcap"
                    if not os.path.isdir(path + "\\traffic"):
                        os.makedirs(path + "\\traffic")
                    traffic_path = os.path.join(path + "\\traffic", traffic_file_name)
                    start_collect_traffic(traffic_path, network_card)
                    time.sleep(2)  # 强制控制睡眠时间,等待tshark 正常启动。
                    print("正常采集新路径", action_sequence_file_path, all_paths[this_all_paths_index])
                    # print(num-1)
                    action_sequence = all_paths[this_all_paths_index]
                    back_flag, click_time_sequences = run_each_path(action_sequence)
                    if back_flag:
                        # 该路径成功采集
                        print("-.-" * 10, "路径采集成功！请稍微，数据存储后按提示进行下一条路径操作")
                        num += 1
                        time.sleep(3)  # 强制控制睡眠时间,把关闭动作的流量采集完毕
                        stop_collect_taffic()
                        write_click_time_sequences(action_sequence_file_path, click_time_sequences)  # 把点击时间序列写入到txt文档中
                    else:
                        print("该路径没有成功采集，退回重新采集")
                        # num = num - 1 #num值不变，继续执行
                store_data(num, this_Applet_name + '_temp_num.bat')  # 存储本次为采集的值
        except Exception as e:
            print("错误类型：", e)


if __name__ == "__main__":
    # read_excel
    # print(read_pickle('mt_all_paths'))#读取存储的文件内容。
    this_Applet_name = 'jxpp'  # 本次采集的小程序简写，根据采集要求设定，不能私自设定。
    batch = 'b1'  # 实验采集的批次，根据采集要求设定，不能私自设定。
    cycles_time = 5  # 本次采集的循环次数，根据采集要求设定，不能私自设定。
    your_network_card = r'\Device\NPF_{A665708D-B95C-40B0-A302-65A7D9A859F6}'  # wifi热点的网卡，根据tshark -D 和 更改适配器选项页面对应查找该
    this_student_name = "zhangsan"  # 数据采集者的名字拼音全拼

    # all_applets_path/jxpp_all_paths_new
    all_paths = read_pickle('all_applets_path/' + this_Applet_name + '_all_paths_new')  # 读取存储的文件内容
    one_sequence_len = len(all_paths)
    max_num = cycles_time * (one_sequence_len)  # 该批次单个数据采集者需要采集的总条数
    print("单个数据采集者，本批次需要采集的路径（记录）总条数：", max_num)

    num_temp = 0  # 采集序号num的复位标志，1表示为复位归零，从新开始计算值，0表示使用采集中间暂存值，不用从新计数，正常批量采集时都是默认值0，在复位后，再次重新运行时设置为0
    num = read_pickle_num(this_Applet_name + '_temp_num.bat', num_temp, MAX_NUM_PATHS=max_num, over_write_flag=False,
                          over_write_value=6)  # 中间暂停时的记录值，当某条记录错误，手动强制则从新采集第over_write_value条，
    control_path_step(all_paths, num, max_num, student_name=this_student_name, batch=batch,
                      Applet_name=this_Applet_name, network_card=your_network_card,
                      one_sequence_len=one_sequence_len)  # 采集者姓名，循环采集次数


