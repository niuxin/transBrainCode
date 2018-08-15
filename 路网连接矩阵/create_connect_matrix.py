# -*-coding:utf-8-*-
# #!/usr/bin/env python
# @file    generateConnectMatrix.py
# @author  XinNiu
# @date    2018-07-30

from __future__ import absolute_import
from __future__ import print_function
import logging
import optparse
import os
import sys
from xml.etree import ElementTree as ET

# @original_connections 路口连接关系 list of (fromLink, fromLane, toLink, toLane)
# @inner_connections 路网内连接关系 list of (fromLink, toLink)
# @start_links 路口出发link集合 list of fromLink
# @end_links 路口结束link集合 list if endLink
# @result_connections 记过集合 list of (fromLink, fromLane, toLink, toLane)

original_connections = []
inner_connections = []
start_links = []
end_links = []
result_connections = []

# parameter
option_parser = optparse.OptionParser()
option_parser.add_option("-n", "--net-file",
                         dest="net_file",
                         help="Network file to work with. Mandatory.",
                         type="string")

option_parser.add_option("-a", "--dict-file",
                         dest="dct",
                         help="detector pinyin.",
                         type="string",
                         default='')

(options, args) = option_parser.parse_args()
if not options.net_file:
    print("Missing arguments")
    option_parser.print_help()
    exit()
if not options.dct:
    print("Missing arguments")
    option_parser.print_help()
    exit()

# file_input = 'D:/pythonWorkPlace/HeFeiSUMO/com/test/test/data2/hefei_area_v12.net.xml'
file_input = options.net_file
tree = ET.ElementTree(file=str(file_input))
for elem in tree.iter(tag='connection'):
    from_link = elem.attrib['from']
    end_link = elem.attrib['to']
    from_lane = elem.attrib['fromLane']
    to_lane = elem.attrib['toLane']
    try:
        tl = elem.attrib['tl']
        original_connections.append((from_link, from_lane, end_link, to_lane))
        start_links.append(from_link)
        end_links.append(end_link)
    except:
        if '_' in from_link or '_' in end_link:
            continue
        else:
            inner_connections.append((from_link, end_link))
del tree

# 集合操作，去重数据
start_links = set(start_links)
end_links = set(end_links)
inner_connections = set(inner_connections)
print(len(start_links))

link_count = {}
for item in start_links:
    link_count[item] = 0
for item in original_connections:
    link_count[item[0]] = max(int(item[1]) + 1, link_count[item[0]])

inner_connections_start_link = set([item[0] for item in inner_connections])

print(len(inner_connections))
print(len(original_connections))

# 判断可以直接相连接的 + 间接相连接的

# 开始真正的表演了
for item in original_connections:
    # print(item)
    # aa = []
    if item[2] in start_links:
        result_connections.append(item)
    else:
        end_link = item[2]
        while end_link not in start_links:
            # 遇到断头处（单向行驶道路），跳出while循环
            if end_link not in inner_connections_start_link:
                break
            else:
                for inner_item in inner_connections:
                    if inner_item[0] == end_link:
                        # aa.append(inner_item[0])
                        end_link = inner_item[1]
                        break
        if end_link in start_links:
            # result_connections.append((item[0], item[1], end_link))
            count_ = link_count[end_link]
            for i in range(count_):
                result_connections.append((item[0], item[1], end_link, str(i)))
print(result_connections)

result = list(set(result_connections))
# 保留原始的数字型detector
f_out = open('connect_matrix_list.txt', 'w')
for item in result:
    s_det = 'e2det_' + item[0] + '_' + item[1]
    e_det = 'e2det_' + item[2] + '_' + item[3]
    if item[0] != item[2]:
        f_out.write(s_det + ',' + e_det + '\n')
f_out.close()

# 使用更新汉语拼音的detector
# read dict data
dict_map = {}
# f = open('D:/pythonWorkPlace/HeFeiSUMO/com/test/test/data2/det_dict_in.txt')
f_path = options.dct
if f_path != '':
    f = open(f_path)
    for line in f:
        tmp = line.strip('\n').split(',')
        dict_map[tmp[0]] = (tmp[1], tmp[2])
    f.close()

    f_out_1 = open('connect_matrix_list_pinyin.txt', 'w')
    for item in result:
        s_det = 'e2det_' + '_'.join(dict_map[item[0]]) + '_' + item[1]
        e_det = 'e2det_' + '_'.join(dict_map[item[2]]) + '_' + item[3]
        if item[0] != item[2]:
            f_out_1.write(s_det + ',' + e_det + '\n')
    f_out_1.close()
else:
    sys.exit()
