import pandas as pd
import numpy as np
from candidate_valleys_tab import candidate_valleys

def sumAMDF(df,k,t):
  sumAx = 0
  i = 0
  while (i < k):
    while (i < t):
      Ax = df.iloc[i,0]
      Ax = checknegative(Ax)
      sumAx  = sumAx + Ax
      i+=1
    Ax = df.iloc[i,0]- df.iloc[i-(t+1),0]
    Ax = checknegative(Ax)
    sumAx  = sumAx + Ax
    i+=1
  return sumAx

def checknegative(Ax):
    if Ax < 0 :
      Ax = -1*(Ax)
    return Ax

def argmin(amdfargx,Esp):
    amdfargxmin = amdfargx.to_numpy()
    argminx = np.argmin(amdfargxmin, axis=0)
    print(Esp+" Tp = ",argminx)
    argminxdf = pd.DataFrame(argminx)
    argminxdf.to_csv('argminxdf '+Esp+' .csv',index=False)
    print("Data saved argminxdf " + Esp)
    return argminxdf

def amdf(df1accbagi3,Esp):
    t_max = 2000
    t_min = 500
    k = 5000

    AmdfAx, index = [], []

    for t in range(t_min, t_max):
      Ax = sumAMDF(df1accbagi3,k,t)
      AMDFAx = (1/k) *(Ax)
      index.append(t)
      AmdfAx.append(AMDFAx)

    amdf = {
                "t": index ,"Ax": AmdfAx
        }
    dataframeamdf = pd.DataFrame(amdf)
    dataframeamdf.to_csv('dataframeamdf '+Esp+' .csv',index=False)
    print("Data saved dataframeamdf "+Esp)

    if dataframeamdf.iloc[0,1] < dataframeamdf.iloc[((t_max-t_min)-1),1]*0.5:
        print("The sensor "+Esp+" is considered as periodic movement")
        amdfargx = dataframeamdf.drop(['t'], axis = 1)
        argminxdf = argmin(amdfargx,Esp)
        candidate_valleys(argminxdf,df1accbagi3,Esp)
    else:
        print("The sensor "+Esp+" is considered as an aperiodic movement")

