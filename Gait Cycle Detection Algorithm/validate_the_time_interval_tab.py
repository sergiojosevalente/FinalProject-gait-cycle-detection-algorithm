import pandas as pd
from amplitudeinterval_tab import amplitudeinterval

def validate_the_time_interval(argminxdf,df1accbagi3,candidatevalley,Esp):

    candivallarrx,intervalx,intervalfallsx = [],[],[]
    
    for i in range(0,len(candidatevalley)):
      if candidatevalley.iloc[i][0] != False:
        candivallarrx.append([i+1,candidatevalley.iloc[i][0]])
    for i in range(0,len(candivallarrx)-1):
      intervalarrx = candivallarrx[i+1][0]-candivallarrx[i][0]
      percentage = (argminxdf.iloc[0,0] /intervalarrx)*100
      intervalx.append([percentage,(candivallarrx[i+1][0]-candivallarrx[i][0]),candivallarrx[i+1][0],candivallarrx[i][0]])
    candivallarrxdf = pd.DataFrame(candivallarrx)
    intervalxdf = pd.DataFrame(intervalx)
    print("Data saved interval "+Esp)
    intervalxdf.columns = ['Percentage', 'Intervalx','Candivallarrx+1','Candivallarrx']
    intervalxdf.to_csv('interval' +Esp+' .csv',index=True)
    for i in range(len(intervalxdf)):
      #if intervalxdf.iloc[i,0] >= 50 and intervalxdf.iloc[i,0]  <= 90:  
      if intervalxdf.iloc[i,0] >= 80 and intervalxdf.iloc[i,0]  <= 120:
        intervalfallsx.append([intervalxdf.iloc[i,0], intervalxdf.iloc[i,1], intervalxdf.iloc[i,3]])
    if len(intervalfallsx)>0:
      intervalfallsxdf = pd.DataFrame(intervalfallsx)
      intervalfallsxdf.columns = ['Percentage', 'Intervalx','Index ke-']
      intervalfallsxdf.to_csv('intervalfallsxdf '+Esp+' .csv',index=True)
      print("Data saved intervalfalls "+Esp)
      amplitudeinterval(candivallarrxdf,df1accbagi3,intervalfallsxdf,Esp,argminxdf)
    else:
      print("interval falls invalid "+Esp)
        