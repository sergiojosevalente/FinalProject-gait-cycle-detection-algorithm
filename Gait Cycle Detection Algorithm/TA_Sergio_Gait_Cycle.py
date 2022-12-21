import paho.mqtt.client as mqtt
import csv
import pandas as pd
import numpy as np  
import statistics
import time
from amdf_tab import amdf

MQTT_ADDRESS = '192.168.43.248'
MQTT_USER = 'sergiocorbymqtt'
MQTT_PASSWORD = 'SergioCorby'
MQTT_TOPIC = 'wban/sensor/#'

AX1,RS1 = [],[]
AX2,RS2 = [],[]

data_size = 5000

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    item = str(msg.payload.decode("utf-8"))

#ESP1 and ESP2
    
#===========================================================#

    if len(AX1) < data_size-1:
        if item[0:8] == "Rssiesp1":
            Rs1 = item[9:16]
            RS1.append(Rs1)
            Ax1 = item[23:]
            AX1.append(Ax1)
    elif len(AX1)==data_size-1 and len(AX2)==0:
        if item[0:8] == "Rssiesp1":
            Rs1 = item[9:16]
            RS1.append(Rs1)
            Ax1 = item[23:]
            AX1.append(Ax1)
            dfaccbagi3 = accbagitiga(AX1,RS1,"Esp1")
            print("=================================")
            startnode1 = time.time()
            amdf(dfaccbagi3,"Esp1")
            endnode1 = time.time()
            totalnode1 = endnode1-startnode1
            if totalnode1 > 60:
                totalnode1 = totalnode1/60
                print("Time execution of Gait Cycle Detection for node1 :", totalnode1 , "Minute")
            else:
                print("Time execution of Gait Cycle Detection for node1 :", totalnode1 , "Second")
    if len(AX2) < data_size-1:
        if item[0:8] == "Rssiesp2":
            Rs2 = item[9:16]
            RS2.append(Rs2)
            Ax2 = item[23:]
            AX2.append(Ax2) 
    elif len(AX2)==data_size-1 and len(AX1)==0:
        if item[0:8] == "Rssiesp2" and len(AX2)==data_size-1:
            Rs2 = item[9:16]
            RS2.append(Rs2)
            Ax2 = item[23:]
            AX2.append(Ax2)
            dfaccbagi3 = accbagitiga(AX2,RS2,"Esp2")
            print("=================================")
            startnode2 = time.time()
            amdf(dfaccbagi3,"Esp2")
            endnode2 = time.time()
            totalnode2 = endnode2-startnode2
            if totalnode2 > 60:
                totalnode2 = totalnode2/60
                print("Time execution of Gait Cycle Detection for node1 :", totalnode2 , "Minute")
            else:
                print("Time execution of Gait Cycle Detection for node1 :", totalnode2 , "Second")
    else:
        if len(AX1)==data_size-1 or len(AX2)==data_size-1 :
            if item[0:8] == "Rssiesp1" and len(AX1)==data_size-1:
                Rs1 = item[9:16]
                RS1.append(Rs1)
                Ax1 = item[23:]
                AX1.append(Ax1)
            elif item[0:8] == "Rssiesp2" and len(AX2)==data_size-1:
                Rs2 = item[9:16]
                RS2.append(Rs2)
                Ax2 = item[23:]
                AX2.append(Ax2)
            if len(AX1)==data_size and len(AX2)==data_size:
                dfaccbagi3Esp1 = accbagitiga(AX1,RS1,"Esp1")
                print("=================================")
                dfaccbagi3Esp2 = accbagitiga(AX2,RS2,"Esp2")
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

#=====================================================================#
    
def accbagitiga(AX,RS,Esp):
    X = []
    dataacc = {"Ax": AX,"Rs":RS}
    dfacc= pd.DataFrame(dataacc)
    
    dfacc.to_csv('dataacc '+Esp+' .csv',index=True)
    print("Data saved acc "+Esp)
    averagerssi = statistics.mean(list(map(float,RS)))
    print(Esp+" AvgRSSI =",averagerssi)

    for i in range(0,len(RS)):
        if i == 0 :
            x = (float(AX[i])+float(AX[i])+float(AX[i]))/3
        elif i == 1:
            x = (float(AX[i])+float(AX[i-1])+float(AX[i]))/3
        else:
            x = (float(AX[i-2])+float(AX[i-1])+float(AX[i]))/3
    
        X.append(x)
        
    dataccbagi3 = {"x": X, "rs":RS}
    dfaccbagi3 = pd.DataFrame(dataccbagi3)
    dfaccbagi3.to_csv('dataaccbagi3 '+Esp+' .csv',index=True)
    print("Data saved acc/3 "+Esp)
    return dfaccbagi3    

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()