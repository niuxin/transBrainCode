# -*-coding:utf-8-*-

# #!/usr/bin/env python
# @file    generateTLSProgram.py
# @author  XinNiu
# @date    2018-07-30

from __future__ import absolute_import
from __future__ import print_function
import optparse
import numpy as np

direction_dict = {}
str_0 = '''由东向南：1
由东向西：2
由东向北：3
由南向西：4
由南向北：5
由南向东：6
由西向北：7
由西向东：8
由西向南：9
由北向东：10
由北向南：11
由北向西：12'''
for item in str_0.split('\n'):
    tmp = item.strip('\n').split('：')
    direction_dict[tmp[0]] = int(tmp[1])


# print(direction_dict)

# read raw tls info return dict of {time_stamp--->(duration_lst, state_lst)}
def read_file(file_path):
    file = open(file_path, encoding='utf-8')
    time_flag = '00:00'
    duration_lst = []
    state_lst = []
    res_dict = {}
    for line in file:
        tmp = line.strip('\n').split('	')
        if tmp[1].split('-')[0] == time_flag:
            duration_lst.append(tmp[2])
            state_lst.append(tmp[3])
        else:
            res_dict[time_flag] = (duration_lst, state_lst)
            duration_lst = []
            state_lst = []
            time_flag = tmp[1].split('-')[0]
            duration_lst.append(tmp[2])
            state_lst.append(tmp[3])
    res_dict[time_flag] = (duration_lst, state_lst)
    del state_lst, time_flag, duration_lst
    return res_dict


# read raw quhua(12) info return exist direction [link;index;s_link;e_link;0] and index_lst
def read_quhua(file_path, road_name):
    file = open(file_path, encoding='utf-8')
    res = []
    index_res = []
    index = 1
    for line in file:
        tmp = line.strip('\n').split(',')
        if tmp[0] == road_name:
            if tmp[2] != 'none' and tmp[3] != 'none':
                lst = []
                lst.append(str(index))
                index_res.append(index)
                lst.append(tmp[2])
                lst.append(tmp[3])
                lst.append('0')
                str_ = ';'.join(lst)
                res.append('link' + ';' + str_)
            index += 1
    return res, index_res


def creat_tls(res_dict, index_res):
    result = []
    for key, value in res_dict.items():
        program_id = key
        duration_lst = value[0]
        state_lst = value[1]
        length = len(duration_lst)
        # initial matrix of shape(length, 12) Red.
        phase_matrix = np.array(['r' for i in range(length * 12)])
        phase_matrix = np.reshape(phase_matrix, (-1, 12))
        # change gry state for 12 direction for  every duration
        for i in range(length):
            # control index(0-11) in state_lst
            index = [direction_dict[item] - 1 for item in state_lst[i].split(',')]
            # yellow
            if duration_lst[i] == '3':
                phase_matrix[i][index] = 'y'
            else:
                phase_matrix[i][index] = 'g'
        res = []
        for i in range(12):
            # change gyg to ggg
            str_ = ';'.join(phase_matrix[:, i])
            for j in range(length):
                str_ = str_.replace('g;y;g', 'g;g;g')
            if str_[-3] == 'g' and str_[-1] == 'y' and str_[0] == 'g':
                str_ = str_[:-1] + 'g'
            if i + 1 in index_res:
                res.append(str(i + 1) + ';' + str_)
        result.append((program_id, res, duration_lst))
    return result


if __name__ == '__main__':

    option_parser = optparse.OptionParser()

    option_parser.add_option("-t", "--tls-file",
                             dest="tls_file",
                             help="traffic light file to work with.",
                             type="string")

    option_parser.add_option("-q", "--quhua-file",
                             dest="qh_file",
                             help="canalization file to work with.",
                             type="string")

    option_parser.add_option("-r", "--road-name",
                             dest="road_name",
                             help="string of road name to work with.",
                             type="string",
                             default='road_name')
    (options, args) = option_parser.parse_args()
    if not options.tls_file:
        print("Missing arguments")
        option_parser.print_help()
        exit()
    if not options.qh_file:
        print("Missing arguments")
        option_parser.print_help()
        exit()

    tls_file = options.tls_file
    res = read_file(tls_file)

    qh_file = options.qh_file
    road_name = options.road_name

    quhua_res, index_res = read_quhua(qh_file, road_name)

    result = creat_tls(res, index_res)
    print(result)
    print(quhua_res)

    # generate csv file
    for item in result:
        time_stamp = str(item[0]).replace(':', '')
        gry_lst = item[1]
        duration_lst = item[2]

        f_input = open('tls/' + road_name + '_' + time_stamp + '.csv', 'w')
        f_input.write('key;' + road_name + '\n')
        f_input.write('subkey;' + time_stamp + '\n')
        f_input.write('offset;' + '0' + '\n')

        # quhua
        for item1 in quhua_res:
            f_input.write(item1 + '\n')
        for item2 in gry_lst:
            f_input.write(item2 + '\n')

        f_input.write('time;' + ';'.join(duration_lst))
        f_input.close()
