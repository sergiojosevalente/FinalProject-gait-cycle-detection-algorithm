import pandas as pd
from validate_the_time_interval_tab import validate_the_time_interval

def candidate_valleys(argminxdf, df1accbagi3,Esp):
    data = df1accbagi3
    X1 = []
    for i in range(0,len(data)-1):
      if i == 0:
        x = (data.iloc[i,0]) < (data.iloc[i,0]) and (data.iloc[i,0]) < (data.iloc[i+1,0])
      else: 
        x = (data.iloc[i,0] < data.iloc[i-1,0]) and (data.iloc[i,0] < data.iloc[i+1,0])
      if x:
        x = data.iloc[i,0]
      X1.append(x)    
      candidatevalley = {"x1": X1}
    candidatevalley = pd.DataFrame(candidatevalley)
    candidatevalley.to_csv('candivall '+Esp+' .csv',index=True)
    print("Data saved candidatevalley " +Esp)
    validate_the_time_interval(argminxdf,df1accbagi3,candidatevalley,Esp)
