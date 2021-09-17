# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:09:00 2021

4-probe station measurements 
2-point measurements symmetric circuit

@author: ayuso
"""

#plot up to 12 files in a folder, different number of points in different measurements, meant for balanced measurements
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)

j=4

dual=True
regre=True
Vfwd=0.1
Vrvs=-0.1
deltaV=0.08
points=7
titulo='M3A01 after 2nd RTA balanced measurements'
colors={0:'C0',1:'C3',2:'C6',3:'C9',4:'C2',5:'C1',6:'C4',7:'C5',8:'C7',9:'C8',10:'k',11:'m',12:'C6',13:'C9',14:'C2',15:'C1',16:'C4',17:'C5',18:'C7',19:'C8',20:'C0',21:'C3',22:'C6',23:'C9',24:'C2',25:'C1',26:'C4',27:'C5',28:'C7',29:'C8'} 

labels={0:'NW1 4-source 1-drain',
        1:'NW2 1-source 2-drain',
        2:'NW4 1-source 2-drain',
        3:'NW6 1-source 2-drain',
        4:'NW3 1-source 4-drain',
        5:'NW3 2-source 3-drain',
        6:'NW4 3-source 2-drain',
        7:'NW4 4-source 3-drain',
        8:'NW4 4-source 3-drain bis',
        9:'NW6 2-source 1-drain',
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
V_fwd={}
V_rvs={}
I_fwd={}
I_rvs={}
slope2Tfwd={}
intercept2Tfwd={}
slope2Trvs={}
intercept2Trvs={}
string2Tfwd={}
string2Trvs={}
    
i=0
for file in files:
    df=pd.read_csv(file)
    matrix=df.to_numpy()
    if dual== True:
        a=int(len(matrix)/2-1)
        currentsS[i]=matrix[0:a,0]
        voltagesS[i]=matrix[0:a,1]
        currentsD[i]=matrix[0:a,2] *-1
        voltagesD[i]=matrix[0:a,3]
        Voltage[i]= voltagesS[i]-voltagesD[i]
        fint = interp1d(Voltage[i], currentsS[i], kind='cubic',assume_sorted=False)    
        V_fwd[i]=np.linspace(Vfwd,Vfwd-deltaV,points)
        V_rvs[i]=np.linspace(Vrvs,Vrvs-deltaV,points)
        I_fwd[i]=np.linspace(Vfwd,Vfwd-deltaV,points)
        I_rvs[i]=np.linspace(Vrvs,Vrvs-deltaV,points)    
        I_fwd[i]=fint(V_fwd[i])/1e-9
        I_rvs[i]=fint(V_rvs[i])/1e-9
        slope2Tfwd[i], intercept2Tfwd[i], r_value12Tfwd, p_value2Tfwd, std_err2Tfwd = stats.linregress(V_fwd[i],I_fwd[i])
        slope2Trvs[i], intercept2Trvs[i], r_value12Trvs, p_value2Trvs, std_err2Trvs = stats.linregress(V_rvs[i],I_rvs[i])    
        string2Tfwd[i]='2 Terminal R = ' + str(round(1000/slope2Tfwd[i], 2)) + ' kOhm'
        string2Trvs[i]='2 Terminal R = ' + str(round(1000/slope2Trvs[i],2)) + ' kOhm'
    else:
        currentsS[i]=matrix[:,0]
        voltagesS[i]=matrix[:,1]
        currentsD[i]=matrix[:,2] *-1
        voltagesD[i]=matrix[:,3]
        Voltage[i]= voltagesS[i]-voltagesD[i]
    i=i+1

n, ax = plt.subplots(figsize=fig_size)
#ax.axvline(x=0.05,color='k')
#ax.axvline(x=-0.05,color ='k')
#ax.set_xlim(-25,13)
#ax.set_ylim(-1,1.5)
for i in range(j):
    if regre==True:
        ax.plot(Voltage[i],currentsS[i]/1e-9,'o',label=labels[i])
        #ax.plot(V_fwd[i],V_fwd[i]*slope2Tfwd[i]+intercept2Tfwd[i],'--',label=string2Tfwd[i])
        ax.plot(V_rvs[i],V_rvs[i]*slope2Trvs[i]+intercept2Trvs[i],'--',label=string2Trvs[i])
        ax.set_title(titulo)
        ax.grid(b='True',which='both',axis='both')
        ax.set_xlabel('Voltage source - Voltage drain (V)')
        ax.set_ylabel('Current (nA)')
        ax.legend()
    else:
        ax.plot(Voltage[i], currentsS[i]/1e-6,label=labels[i])  #+' S')
        #ax.plot(Voltage[i], currentsD[i]/1e-6,label=labels[i]+' D')
        ax.set_title(titulo)
        ax.grid(b='True',which='both',axis='both')
        ax.set_xlabel('Voltage source - Voltage drain (V)')
        ax.set_ylabel('Current (uA)')
        ax.legend()
        


#%% plot by contacts
    
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)

j=1
titulo='M3A01 2ndRTA balanced measurements'
colors={0:'C0',1:'C3',2:'C9',3:'C6'} 
labels={0:'4 source',
        1:'1 drain',
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
    ax.plot(Voltage[i], currents[i]/1e-6,label=labels[i],color=colors[i])
    ax.set_title(titulo)
    ax.grid(b='True',which='both',axis='both')
    ax.set_xlabel('Voltage source - Voltage drain (V)')
    ax.set_ylabel('Current (uA)')
    ax.legend(loc='lower right')
    



#%% Slope regression: Linear regresion of the IV curve, being x voltage, meaning resistance = 1/slope
#1/slope already in MOhm, since the linear regression was done with I in uA
    #FOR COMPLIANCE MEASUREMENTS: make sure to choose the adecuate range of SD voltage
    #to avoid unsorted arrays 
import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

fig_size = (15,10)
j = plt.figure(figsize=fig_size)

file_name='M3A05_2RTA_NW4_4Source_3Drain_3VSD_bis.csv'
dual=True
Vfwd=-0.7
Vrvs=-1.7
deltaV=0.25
points=5

colors={0:'C0',1:'C3',2:'C9',3:'C6'} 
legend='NW4 4 source 3 drain'

directory=os.getcwd()
file=directory+'\\'+file_name
df1=pd.read_csv(file)
#df=pd.read_csv(r'C:\Users\ayuso\Documents\Measurements\4probestation\I04\I04_afterRTAs_Vsd=4V_contacts1to4.csv')
matrix1=df1.to_numpy()
if dual == True:
    a=int(len(matrix1)/2-1)
    currentS=matrix1[0:a,0]
    currentD=matrix1[0:a,2]
    voltage_SD=matrix1[0:a,4]
    currentnAS=currentS/1e-9         
    currentuAS=currentS/1e-6
    currentnAD=currentD/1e-9         
    currentuAD=currentD/1e-6
else:
    currentS=matrix1[0,0]
    currentD=matrix1[0,2]
    voltage_SD=matrix1[0,4]
    currentnAS=currentS/1e-9         
    currentuAS=currentS/1e-6
    currentnAD=currentD/1e-9         
    currentuAD=currentD/1e-6
    
fint = interp1d(voltage_SD, currentS, kind='cubic',assume_sorted=False)    
V_fwd=np.linspace(Vfwd,Vfwd-deltaV,points)
V_rvs=np.linspace(Vrvs,Vrvs-deltaV,points)
I_fwd=np.linspace(Vfwd,Vfwd-deltaV,points)
I_rvs=np.linspace(Vrvs,Vrvs-deltaV,points)    
for i in range(V_fwd.size):
    I_fwd[i]=fint(V_fwd[i])/1e-6
    I_rvs[i]=fint(V_rvs[i])/1e-6
    
slope2Tfwd, intercept2Tfwd, r_value12Tfwd, p_value2Tfwd, std_err2Tfwd = stats.linregress(V_fwd,I_fwd)
slope2Trvs, intercept2Trvs, r_value12Trvs, p_value2Trvs, std_err2Trvs = stats.linregress(V_rvs,I_rvs)    


string2Tfwd='2 Terminal R = ' + str(round(1000/slope2Tfwd, 3)) + ' kOhm'
string2Trvs='2 Terminal R = ' + str(round(1000/slope2Trvs,3)) + ' kOhm'

title1=file_name.strip('.csv')
plt.plot(voltage_SD,currentuAS,'C0o',label=legend)
plt.plot(V_fwd,V_fwd*slope2Tfwd+intercept2Tfwd,'--',label=string2Tfwd)
plt.plot(V_rvs,V_rvs*slope2Trvs+intercept2Trvs,'--',label=string2Trvs)
plt.title(title1)
plt.grid(b='True',which='both',axis='both')
plt.xlabel('Voltage SD (V)')
plt.ylabel('Current (uA)')
plt.legend()
plt.show()


#%% Diff resistance
    ##WORK IN PROGRESS
    
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
    


h = plt.figure(figsize=fig_size)
h = diff_resistance('I06_5thRTA_contact4GNDto3SMU_1-5Vsd.csv', h,'r-','5thRTA')