# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:09:00 2021

@author: ayuso
"""
# plot up to 12 files in a folder, different number of points in different measurements, meant for balanced measurements
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)

j=6
titulo='E04 before RTA balanced measurements'
colors={0:'C0',1:'C3',2:'C6',3:'C9',4:'C2',5:'C1',6:'C4',7:'C5',8:'C7',9:'C8',10:'C0',11:'C3',12:'C6',13:'C9',14:'C2',15:'C1',16:'C4',17:'C5',18:'C7',19:'C8',20:'C0',21:'C3',22:'C6',23:'C9',24:'C2',25:'C1',26:'C4',27:'C5',28:'C7',29:'C8'} 

labels={0:'NW2 4-source 1-drain',
        1:'NW3 2-source 3-drain',
        2:'NW3 4-source 1-drain',
        3:'NW4 4-source 1-drain',
        4:'NW5 1-source 4-drain',
        5:'NW6 1-source 4-drain',
        6:'3-source 2-drain',
        7:'3-source 4-drain',
        8:'4-source 1-drain',
        9:'4-source 2-drain',
        10:'4-source 3-drain'
        } 

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
ax.set_xlim(-10,5)
#ax.set_ylim(-1,1.5)
for i in range(j):
    ax.plot(Voltage[i], currentsS[i]/1e-9,label=labels[i]+' S')
    ax.plot(Voltage[i], currentsD[i]/1e-9,label=labels[i]+' D')
    ax.set_title(titulo)
    ax.grid(b='True',which='both',axis='both')
    ax.set_xlabel('Voltage source - Voltage drain (V)')
    ax.set_ylabel('Current (nA)')
    ax.legend(loc='upper left')
        

#%% plot individual measurements
    
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)

j=6
titulo='E04 before RTA balanced measurements'
colors={0:'C0',1:'C3',2:'C6',3:'C9',4:'C2',5:'C1',6:'C4',7:'C5',8:'C7',9:'C8',10:'C0',11:'C3',12:'C6',13:'C9',14:'C2',15:'C1',16:'C4',17:'C5',18:'C7',19:'C8',20:'C0',21:'C3',22:'C6',23:'C9',24:'C2',25:'C1',26:'C4',27:'C5',28:'C7',29:'C8'} 

labels={0:'NW1 4-source 1-drain',
        1:'NW2 4-source 1-drain',
        2:'NW3 2-source 3-drain',
        3:'NW3 4-source 1-drain',
        4:'NW4 4-source 1-drain',
        5:'NW5 1-source 4-drain',
        6:'NW6 1-source 4-drain',
        7:'3-source 2-drain',
        8:'3-source 4-drain',
        9:'4-source 1-drain',
        10:'4-source 2-drain',
        11:'4-source 3-drain'
        } 

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
ax.set_xlim(-10,5)

i=6

ax.plot(Voltage[i], currentsS[i]/1e-9,label=labels[i]+' S', color='C0')
ax.plot(Voltage[i], currentsD[i]/1e-9,label=labels[i]+' D', color='C3')
ax.set_title(titulo + ' NW6')
ax.grid(b='True',which='both',axis='both')
ax.set_xlabel('Voltage source - Voltage drain (V)')
ax.set_ylabel('Current (nA)')
ax.legend(loc='upper left')


