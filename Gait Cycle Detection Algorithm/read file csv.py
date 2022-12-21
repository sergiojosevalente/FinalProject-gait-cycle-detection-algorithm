import csv
import pandas as pd
from amdf_tab import amdf
import time

dfaccbagi3Esp1 = pd.read_csv (r"dataaccbagi3 Esp1 .csv")
dfaccbagi3Esp1 = dfaccbagi3Esp1.drop(['Unnamed: 0'], axis=1)
print("=================================")
startnode1 = time.time()
amdf(dfaccbagi3Esp1,"Esp1")
endnode1 = time.time()
totalnode1 = endnode1-startnode1
if totalnode1 > 60:
    totalnode1 = totalnode1/60
    print("Time execution of Gait Cycle Detection for node1 :", totalnode1 , "Minute")
else:
    print("Time execution of Gait Cycle Detection for node1 :", totalnode1 , "Second")
print("=================================")

dfaccbagi3Esp2 = pd.read_csv (r"dataaccbagi3 Esp2 .csv")
dfaccbagi3Esp2 = dfaccbagi3Esp2.drop(['Unnamed: 0'], axis=1)
startnode2 = time.time()
amdf(dfaccbagi3Esp2,"Esp2")
endnode2 = time.time()
totalnode2 = endnode2-startnode2
if totalnode2 > 60:
    totalnode2 = totalnode2/60
    print("Time execution of Gait Cycle Detection for node2 :", totalnode2 , "Minute")
else:
    print("Time execution of Gait Cycle Detection for node2 :", totalnode2 , "Second")
print("=================================")
