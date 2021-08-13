# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:09:00 2021

4-probe station measurements 

@author: ayuso
"""
# plot up to 12 files in a folder, different number of points in different measurements, meant for balanced measurements
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)

j=4
titulo='I1 before RTA balanced measurements 15.07'
colors={0:'C0',1:'C3',2:'C6',3:'C9',4:'C2',5:'C1',6:'C4',7:'C5',8:'C7',9:'C8',10:'C0',11:'C3',12:'C6',13:'C9',14:'C2',15:'C1',16:'C4',17:'C5',18:'C7',19:'C8',20:'C0',21:'C3',22:'C6',23:'C9',24:'C2',25:'C1',26:'C4',27:'C5',28:'C7',29:'C8'} 

labels={0:'-source 1-drain custom',
        1:'4-source 1-drain custom bis',
        2:'4-source 1-drain normal',
        3:'4-source 1-drain normal bis',
        4:'2-source 3-drain',
        5:'2-source 4-drain',
        6:'3-source 1-drain',
        7:'3-source 2-drain',
        8:'3-source 4-drain',
        9:'4-source 1-drain',
        10:'4-source 2-drain',
        11:'4-source 3-drain'
        } 


# labels={0:'4-source 1-drain quiet',
#         1:'4-source 1-drain quiet dual sweep',
#         } 

files=glob.glob('*.csv')
currentsS={}
voltagesS={}
currentsD={}
voltagesD={}
Voltage={}
    
i=0
for file in files:
    df=pd.read_csv(file)
    matrix=df.to_numpy()
    currentsS[i]=matrix[:,0]
    voltagesS[i]=matrix[:,1]
    currentsD[i]=matrix[:,2] *-1
    voltagesD[i]=matrix[:,3]
    Voltage[i]= voltagesS[i]-voltagesD[i]
    i=i+1
n, ax = plt.subplots(figsize=fig_size)
#ax.axvline(x=0.05,color='k')
#ax.axvline(x=-0.05,color='k')
#ax.set_xlim(-25,13)
#ax.set_ylim(-1,1.5)
for i in range(j):
    ax.plot(Voltage[i], currentsS[i]/1e-9,label=labels[i]+' S')
    ax.plot(Voltage[i], currentsD[i]/1e-9,label=labels[i]+' D')
    ax.set_title(titulo)
    ax.grid(b='True',which='both',axis='both')
    ax.set_xlabel('Voltage source - Voltage drain (V)')
    ax.set_ylabel('Current (nA)')
    ax.legend(loc='upper left')
        


#%% plot by contacts
    
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)

j=2
titulo='I12 before RTA balanced measurements contacts 1 and 4'
colors={0:'C0',1:'C3',2:'C9',3:'C6'} 
labels={0:'1 Idrain',
        1:'4 Isource',
        # 2:'4 Isource',
        # 3:'3 Idrain',
        } 
files=glob.glob('*.csv')
currents={}
voltages={}
Voltage={} #source-drain, drain current x-1
i=0
for file in files:
    df=pd.read_csv(file)
    matrix=df.to_numpy()
    currents[i]=matrix[:,0]  #Isource 
    voltages[i]=matrix[:,1]  #Vsource 
    currents[i+1]=matrix[:,2]*-1  #Idrain 
    voltages[i+1]=matrix[:,3]  #Vdrain
    Voltage[i]= voltages[i]-voltages[i+1] 
    Voltage[i+1]= voltages[i]-voltages[i+1] 
    i=i+2
n, ax = plt.subplots(figsize=fig_size)
for i in range(j):
    ax.plot(Voltage[i], currents[i]/1e-9,label=labels[i],color=colors[i])
    ax.set_title(titulo)
    ax.grid(b='True',which='both',axis='both')
    ax.set_xlabel('Voltage source - Voltage drain (V)')
    ax.set_ylabel('Current (nA)')
    ax.legend(loc='lower right')
    

#%% Diff resistance
import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

fig_size = (15,10)
f = plt.figure(figsize=fig_size)

#dV=

df1=pd.read_csv(file)
diff_res1=matrix1[0,4]
# currentnA1=current1/1e-9
# currentuA1=current1/1e-6
    dV_1=np.diff(voltage_SD1)
    dI_1=np.diff(current1)
    diffR2T_1=dV_1/dI_1
    title1=file_name.strip('.csv')
    plt.title(title1+'_DiffResistance')
    plt.plot(currentuA1[0:-1],diffR2T_1/1e6,markers,label=legend)
    # plt.plot(currentuA0,R2T_0/1e3,label='2Terminal res')
    # plt.plot(currentuA0,R4T_0/1e3,label='4Terminal res')
    plt.grid(b='True',which='both',axis='both')
    plt.ylabel('Resistance (MOhm)')
    plt.xlabel('Current (uA)')
    plt.legend(loc="upper right")
    # plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))
    
    return(f)

h = plt.figure(figsize=fig_size)
h = diff_resistance('I06_5thRTA_contact4GNDto3SMU_1-5Vsd.csv', h,'r-','5thRTA')