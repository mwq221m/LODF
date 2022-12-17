import numpy as np
import pandas as pd
#import networkx as nx
import time

class LODF():
    def __init__(self,bus_data,branch_data):
        self.version='1.0.1'
        self.bus_data=bus_data
        self.branch_data=branch_data
        self.bus_num=len(self.bus_data)
        self.branch_num=len(self.branch_data)
        self.lodf_matrix=np.zeros((self.branch_num,self.branch_num))
        self.B=np.zeros((self.bus_num,self.bus_num))
        self.B_apostrophe=np.zeros((self.bus_num-1,self.bus_num-1))

        for i in range(self.branch_num):
            temp=self.branch_data.iloc[i]
            status=temp['status']
            x=temp['x']
            start=temp['start']
            end=temp['end']
            if status==1:
                start_idx=int(start)-1
                end_idx=int(end)-1
                b=1/x
                self.B[start_idx,start_idx]+=b
                self.B[end_idx,end_idx]+=b
                self.B[start_idx,end_idx]+=-b
                self.B[end_idx,start_idx]+=-b
        self.B_apostrophe=self.B[:-1,:-1].copy()
        self.X=np.linalg.inv(self.B_apostrophe)

    def generate_m(self,start,end):
        m=np.zeros(self.bus_num-1)
        start_idx=int(start)-1
        end_idx=int(end)-1
        if start!=self.bus_num:#挑选最大编号节点当做参考节点
            m[start_idx]=1
        if end!=self.bus_num:
            m[end_idx]=-1
        return m

    def run(self):
        for i in range(self.branch_num):
            for j in range(self.branch_num):
                if i!=j:
                    tempi=self.branch_data.iloc[i]
                    tempj=self.branch_data.iloc[j]
                    xi=tempi['x']
                    xj=tempj['x']
                    # print('xi',xi)
                    # print('xj',xj)
                    starti=tempi['start']
                    endi=tempi['end']
                    startj=tempj['start']
                    endj=tempj['end']
                    mi=self.generate_m(start=starti,end=endi)
                    mj=self.generate_m(start=startj,end=endj)
                    xij=mi.reshape(1,-1)@self.X@mj.reshape(-1,1)
                    xij=float(xij)
                    #print('xij',xij)
                    xjj=mj.reshape(1,-1)@self.X@mj.reshape(-1,1)
                    xjj=float(xjj)
                    #print('xjj',xjj)
                    self.lodf_matrix[i,j]=(xij/xi)/(1-xjj/xj)
















if __name__=='__main__':
    branch_data = pd.read_excel('test.xlsx', sheet_name=0)
    bus_data = pd.read_excel('test.xlsx', sheet_name=1)
    start=time.time()
    obj=LODF(bus_data=bus_data,branch_data=branch_data)
    # print(obj.B)
    # print(obj.B_apostrophe)
    # print(obj.generate_m(start=1,end=2))
    # print(obj.generate_m(start=1, end=3))
    # print(obj.generate_m(start=3, end=2))
    #print(obj.run())
    obj.run()
    print(obj.lodf_matrix)
    end=time.time()
    print('运行时间',end-start)
    '''
    对于度只有2的节点，相邻支路开断分布因子只有1或-1，由拓扑结构决定与支路参数无关
    '''
