参数介绍
1."-t", "--tls-file" 信号灯原始相位相序程序文件地址，按时间排列整齐。文件‘huizhou_huangshan_tls.txt’
2."-q", "--quhua-file" 渠化方案数据文件地址，通俗表述：东南西北，左直右 12 方位link连接关系，只关注到edge等级。文件‘huizhou_huangshan_quhua.txt’
3."-r", "--road-name" 涉及的道路名称，在渠化文件中进行查找相关roadName的信息，再生成文件时决定文件名称、内容key；roadName等。
文件在统计目录
运行脚本 python creat_tls.py -t huizhou_huangshan_tls.txt -q huizhou_huangshan_quhua.txt -r huizhou_huangshan
结果文件：按照roadName+timestamp生成对应不同时间段的信号灯csv文件。




运行脚本 tls_csv2SUMO.py tls3.csv hefei_area_v12.net.xml
生成真实可用信号灯
注意第一个脚本中用到的 roadName 在路网中依然是数字表示的，需更改一下key;roadName。