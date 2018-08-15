参数介绍
1."-n", "--net-file" 路网文件位置 ‘hefei_area_v12.net.xml’
2."-a", "--dict-file" det_dict文件位置 ‘det_dict_in.txt’；该参数可以不提供，表示直接用路网中的linkId组成的原始检测器表示连接关系。若提供则多生成一份有意义的检测器连接关系。
参数文件在同级目录中

运行脚本：python create_connect_matrix.py -n hefei_area_v12.net.xml -a det_dict_in.txt

结果保存在统计目录下，保存形式如下
detectorID_1,detectorID_2   表示两个检测器有连接关系。


