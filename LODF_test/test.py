from dlpf import DLPF
from lodf import LODF
import numpy as np
import pandas as pd
import time
'''
测试rts79系统是否出现明显的bug
'''

branch_data = pd.read_excel('rts79_test.xlsx', sheet_name=0)
bus_data = pd.read_excel('rts79_test.xlsx', sheet_name=1)
start=time.time()
obj=LODF(bus_data=bus_data,branch_data=branch_data)
obj.run()
end=time.time()
print(obj.lodf_matrix)
print('运行时间',end-start)