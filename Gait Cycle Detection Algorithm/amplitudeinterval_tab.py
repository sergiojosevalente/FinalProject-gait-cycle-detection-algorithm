import pandas as pd

def amplitudeinterval(candivallarrxdf,df1accbagi3,intervalfallsxdf,Esp,argminxdf):
    amplitudeintervalx= []
    a = 0
    for i in range(0,len(candivallarrxdf)):
      for a in range(0,len(intervalfallsxdf)):
        if intervalfallsxdf.iloc[a,2] == candivallarrxdf.iloc[i,0]:
          amplitudecandivall = intervalfallsxdf.iloc[a,2],candivallarrxdf.iloc[i,1]
          amplitudeintervalx.append(amplitudecandivall)
    if len(amplitudeintervalx)>0:
        amplitudeintervalxdf = pd.DataFrame(amplitudeintervalx)
        amplitudeintervalxdf.columns = ['Index Falls ke-','X']
        amplitudeintervalxdf.to_csv('amplitudeintervalxdf '+Esp+' .csv',index=True)
        print("Data saved amplitudeintervalxdf "+Esp)
        nearestpickamplitude(amplitudeintervalxdf,df1accbagi3,intervalfallsxdf,Esp,argminxdf)
    else:
        print("No data from Amplitude interval "+Esp)
    
    
def nearestpickamplitude(amplitudeintervalxdf,df1accbagi3,intervalfallsxdf,Esp,argminxdf):
    nearestpickamplitudex = [] 
    for i in range (0,len(intervalfallsxdf)-1):
        minamplitudeinterval,maxamplitudeinterval = intervalfallsxdf.iloc[i,2],intervalfallsxdf.iloc[i+1,2]
        minamplitude,index = df1accbagi3.iloc[minamplitudeinterval+1,0],minamplitudeinterval+1
        for j in range (minamplitudeinterval,maxamplitudeinterval):
            if minamplitude > df1accbagi3.iloc[j+2,0]:
              minamplitude,index =  df1accbagi3.iloc[j+2,0],j+2
        nearestpickamplitudex.append([minamplitude,index])
    if len(nearestpickamplitudex)>0:
        nearestpickamplitudexdf = pd.DataFrame(nearestpickamplitudex)
        nearestpickamplitudexdf.columns = ['AmplitudeMaks','Index ke-']
        nearestpickamplitudexdf.to_csv('nearestpickamplitudexdf '+Esp+' .csv',index=True)
        print("Data saved nearestpickamplitudexdf "+Esp)
        validvalley(amplitudeintervalxdf,nearestpickamplitudexdf,Esp,argminxdf)
    else:
        print("No data from Nearest Valid Amplitude "+Esp)
        
        
def validvalley(amplitudeintervalxdf,nearestpickamplitudexdf,Esp,argminxdf):
    validvalley = []
    for i in range(0,len(amplitudeintervalxdf)-1):
      if i == 0:
        if amplitudeintervalxdf.iloc[i,1] < nearestpickamplitudexdf.iloc[i,0]*0.25:
          validvalley.append(amplitudeintervalxdf.iloc[i,0])
      elif i == len(amplitudeintervalxdf):
        if amplitudeintervalxdf.iloc[i,1] < nearestpickamplitudexdf.iloc[i,0]*0.25:
          validvalley.append(amplitudeintervalxdf.iloc[i,0])
      else:
          nearestpickleft,nearestpickright = amplitudeintervalxdf.iloc[i,0] - nearestpickamplitudexdf.iloc[i-1,1], nearestpickamplitudexdf.iloc[i,1] - amplitudeintervalxdf.iloc[i,0]
          if nearestpickleft < nearestpickright:
            nearestpick = nearestpickamplitudexdf.iloc[i-1,0]
          else:
            nearestpick = nearestpickamplitudexdf.iloc[i,0]
          if amplitudeintervalxdf.iloc[i,1] < nearestpick*0.25:
            validvalley.append(amplitudeintervalxdf.iloc[i,0])            
    if len(validvalley)>0:
      validvaleyxdf = pd.DataFrame(validvalley)
      validvaleyxdf.columns = ['Index Ke-' ]
      print("Phase is the time of the Last valid valley "+Esp)
      phase = len(validvaleyxdf)
      print("Phase "+Esp+" =",validvaleyxdf.iloc[phase-1,0])
      degrad = (((int(validvaleyxdf.iloc[phase-1,0]/argminxdf.iloc[0,0]))*argminxdf.iloc[0,0]))
      degree = ((validvaleyxdf.iloc[phase-1,0]-degrad)/argminxdf.iloc[0,0])*360
      radian = ((validvaleyxdf.iloc[phase-1,0]-degrad)/argminxdf.iloc[0,0])*2
      print("Degree for "+Esp+" =",degree, "Degrees")
      print("Radian for "+Esp+" =",radian, "Phi Radians")
      validvaleyxdf.to_csv('validvaleyx '+Esp+' .csv',index=True)
      print("Valid valley of "+Esp+" x is stored.")
    else:
      print("interval falls invalid in "+Esp)