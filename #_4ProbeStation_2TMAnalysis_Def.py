# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:22:20 2021

@author: ayuso
"""

import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

fig_size = (15,10)
f = plt.figure(figsize=fig_size)

def plot_2TM_probestation(file_name,fig=f,markers='',legend=''):
    directory=os.getcwd()
    file=directory+'\\'+file_name
    df1=pd.read_csv(file)
    #df=pd.read_csv(r'C:\Users\ayuso\Documents\Measurements\4probestation\I04\I04_afterRTAs_Vsd=4V_contacts1to4.csv')
    matrix1=df1.to_numpy()
    time1=matrix1[:,0]
    current1=matrix1[:,1]
    voltage_SD1=matrix1[:,2]
    resistance1=matrix1[0,3]
    diff_res1=matrix1[0,4]
    currentnA1=current1/1e-9
    currentuA1=current1/1e-6
    title1=file_name.strip('.csv')
    plt.plot(voltage_SD1,currentuA1,markers,label=legend)
    plt.title(title1)
    plt.grid(b='True',which='both',axis='both')
    plt.xlabel('Voltage SD (V)')
    plt.ylabel('Current (uA)')
    plt.legend(loc="upper left")
    
    return(f)

f=plot_2TM_probestation('I06_5thRTA_contact1GNDto3SMU_1-5Vsd.csv',f,'ro','5thRTA')

#plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))

#plt.ticklabel_format(axis='y',style='scientific',scilimits=(0,0))
#%% Linear regresion of the IV curve, being x voltage, meaning resistance = 1/slope
#1/slope already in MOhm, since the linear regression was done with I in uA
import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

fig_size = (15,10)
j = plt.figure(figsize=fig_size)

def LinReg_2TM_probestation(file_name,Vfwd,Vrvs,deltaV,points,hysteresis=True):
    directory=os.getcwd()
    file=directory+'\\'+file_name
    df1=pd.read_csv(file)
    #df=pd.read_csv(r'C:\Users\ayuso\Documents\Measurements\4probestation\I04\I04_afterRTAs_Vsd=4V_contacts1to4.csv')
    matrix1=df1.to_numpy()
    if hysteresis == True:
        a=int(len(matrix1)/2-1)
        time1=matrix1[0:a,0]
        current1=matrix1[0:a,1]
        voltage_SD1=matrix1[0:a,2]
        resistance1=matrix1[0,3]
        diff_res1=matrix1[0,4]
        currentnA1=current1/1e-9         
        currentuA1=current1/1e-6
    else:
        time1=matrix1[:,0]
        current1=matrix1[:,1]
        voltage_SD1=matrix1[:,2]
        resistance1=matrix1[0,3]
        diff_res1=matrix1[0,4]
        currentnA1=current1/1e-9
        currentuA1=current1/1e-6
    fint = interp1d(voltage_SD1, current1, kind='cubic',assume_sorted=False)    
    V_fwd=np.linspace(Vfwd,Vfwd-deltaV,points)
    V_rvs=np.linspace(Vrvs,Vrvs-deltaV,points)
    I_fwd=np.linspace(Vfwd,Vfwd-deltaV,points)
    I_rvs=np.linspace(Vrvs,Vrvs-deltaV,points)    
    for i in range(V_fwd.size):
        I_fwd[i]=fint(V_fwd[i])/1e-6
        I_rvs[i]=fint(V_rvs[i])/1e-6
    slope2Tfwd, intercept2Tfwd, r_value12Tfwd, p_value2Tfwd, std_err2Tfwd = stats.linregress(V_fwd,I_fwd)
    slope2Trvs, intercept2Trvs, r_value12Trvs, p_value2Trvs, std_err2Trvs = stats.linregress(V_rvs,I_rvs)    
    return(voltage_SD1,currentuA1,V_fwd,slope2Tfwd,intercept2Tfwd,V_rvs,slope2Trvs,intercept2Trvs)


(voltage_SD1,currentuA1,V_fwd,slope2Tfwd,intercept2Tfwd,V_rvs,slope2Trvs,intercept2Trvs) = LinReg_2TM_probestation('I07_contact1GNDto2SMU_1-5Vsd_bis.csv',0.7,-0.5,0.25,5,hysteresis=True)

#plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))
#plt.ticklabel_format(axis='y',style='scientific',scilimits=(0,0))


#%%
#1/slope already in MOhm, since the linear regression was done with I in uA
import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

def Plots_2TM_probestation(file_name,Vfwd,Vrvs,deltaV,points,markers='',legend='',hysteresis=True):
    (voltage_SD1,currentuA1,V_fwd,slope2Tfwd,intercept2Tfwd,V_rvs,slope2Trvs,intercept2Trvs)=LinReg_2TM_probestation(file_name, Vfwd, Vrvs, deltaV, points, hysteresis)
    string2Tfwd='2 Terminal R = ' + str(round(1/slope2Tfwd, 3)) + ' MOhm'
    string2Trvs='2 Terminal R = ' + str(round(1/slope2Trvs, 3)) + ' MOhm'
    title1=file_name.strip('.csv')
    plt.plot(voltage_SD1,currentuA1,markers,label=legend)
    plt.plot(V_fwd,V_fwd*slope2Tfwd+intercept2Tfwd,'b--',label=string2Tfwd)
    plt.plot(V_rvs,V_rvs*slope2Trvs+intercept2Trvs,'g--',label=string2Trvs)
    plt.title(title1)
    plt.grid(b='True',which='both',axis='both')
    plt.xlabel('Voltage SD (V)')
    plt.ylabel('Current (uA)')
    plt.legend(loc="upper left")
    plt.show()
    return(j)


j = Plots_2TM_probestation('I09_contact2GNDto4SMU_3Vsd.csv',2-2,0.25,5,'ro','5thRTA',hysteresis=False)
#plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))
#plt.ticklabel_format(axis='y',style='scientific',scilimits=(0,0))


#%% Diff resistance
import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

def diff_resistance(file_name,fig=f,markers='',legend=''):
    directory=os.getcwd()
    file=directory+'\\'+file_name
    df1=pd.read_csv(file)
    #df=pd.read_csv(r'C:\Users\ayuso\Documents\Measurements\4probestation\I04\I04_afterRTAs_Vsd=4V_contacts1to4.csv')
    matrix1=df1.to_numpy()
    time1=matrix1[:,0]
    current1=matrix1[:,1]
    voltage_SD1=matrix1[:,2]
    resistance1=matrix1[0,3]
    diff_res1=matrix1[0,4]
    currentnA1=current1/1e-9
    currentuA1=current1/1e-6
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


#%% plot up to 10 files in a folder, different number of points in different measurements, meant for after RTA
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,10)


colors={0:'C0',1:'C3',2:'C6',3:'C9',4:'C2',5:'C1',6:'C4',7:'C5',8:'C7',9:'C8'} 
#colors={0:'C3',1:'C6',2:'C9',3:'C2',4:'C4'}

def multiplePlots(j,titulo, labels):
    files=glob.glob('*.csv')
    times={}
    currents={}
    voltages={}
    
    i=0
    for file in files:
        df=pd.read_csv(file)
        matrix=df.to_numpy()
        times[i]=matrix[:,0]
        currents[i]=matrix[:,1]
        voltages[i]=matrix[:,2]
        i=i+1
    n, ax = plt.subplots(figsize=fig_size)
    for i in range(j):
        ax.plot(voltages[i], currents[i]/1e-6,label=labels[i],color=colors[i])
        ax.set_title(titulo)
        ax.grid(b='True',which='both',axis='both')
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Current (uA)')
        ax.legend(loc='upper left')
        
    return(n)


#labels={0:'contact1to2',1:'contact1to3',2:'contact1to4',3:'contact2to3',4:'contact2to4',5:'contact3to4'}
#labels={0:'contact1to3',1:'contact1to4',2:'contact2to3',3:'contact2to4',4:'contact3to4'}
labels={0:'1st try',1:'2nd try',2:'3rd try',3:'4th try',4:'5th try',5:'6th try',6:'7th try',7:'8th try',8:'9th try',9:'10th try'}
multiplePlots(8,'contact 3 to 4',labels)
#plt.text(1.2,1.2,'R=1.8 kOhm')
#plt.text(-1.9,-2.5,'R=1.03 MOhm')
# plt.text(1.5,2,'R=0.15 MOhm')
# plt.text(-1.3,-5.5,'R=0.14 MOhm')
# plt.text(-1.5,0,'R=2.3 MOhm')


#%%
#plot of all files in a folder, different sizes of arrays, meant for same pair of contacts
#careful with hysteresis, all files must have the same hysteresys value
#1/slope already in MOhm, since the linear regression was done with I in uA

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 17})
fig_size = (15,15)



colors={0:'C0',1:'C3',2:'C6',3:'C9',4:'C2',5:'C1',6:'C4',7:'C5',8:'C7',9:'C8'} 
#colors={0:'C0',1:'C6',2:'C9',3:'C2'}
#colors={0:'C0',1:'C6',2:'C9'}
def multiplePlots_LinReg(j,titulo, labels, Vfwd, Vrvs, deltaV, points, hysteresis=True):
    files=glob.glob('*.csv')
    times={}
    currents={}
    voltages={}
    V_fwd={}
    slope2Tfwd={}
    intercept2Tfwd={}
    V_rvs={}
    slope2Trvs={}
    intercept2Trvs={}
    string2Tfwd={}
    string2Trvs={}
    i=0
    for file in files:
        df=pd.read_csv(file)
        matrix=df.to_numpy()
        times[i]=matrix[:,0]
        currents[i]=matrix[:,1]
        voltages[i]=matrix[:,2]
        (V,I,V_fwd[i],slope2Tfwd[i],intercept2Tfwd[i],V_rvs[i],slope2Trvs[i],intercept2Trvs[i])=LinReg_2TM_probestation(file, Vfwd[i], Vrvs[i], deltaV, points, hysteresis)
        string2Tfwd[i]='2TM fwd R = ' + str(round(1/slope2Tfwd[i],2)) + ' MOhm'
        string2Trvs[i]='2TM rvs R = ' + str(round(1/slope2Trvs[i],2)) + ' MOhm'
        i=i+1
    n, ax = plt.subplots(figsize=fig_size)
    for x in range(j):
        # ax.set_xlim([-0.006,0.004])
        # ax.set_ylim([-0.2,2])
        ax.plot(voltages[x], currents[x]/1e-6,label=labels[x],color=colors[x])
        ax.plot(V_fwd[x],V_fwd[x]*slope2Tfwd[x]+intercept2Tfwd[x],'--',label=string2Tfwd[x])
        ax.plot(V_rvs[x],V_rvs[x]*slope2Trvs[x]+intercept2Trvs[x],'--',label=string2Trvs[x])
        ax.set_title(titulo)
        ax.grid(b='True',which='both',axis='both')
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Current (uA)')
        ax.legend(loc='upper left')
        
    return(n)
Vfwd={0:1,1:3,2:3,3:3,4:3,5:2,6:2.8,7:3,8:3,9:3}
Vrvs={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:1,8:0,9:0}
deltaV=0.6
points=5
labels={0:'1st try',1:'2nd try',2:'3rd try',3:'4th try',4:'5th try',5:'6th try',6:'7th try',7:'8th try',8:'9th try',9:'10th try'}
multiplePlots_LinReg(10,'contact 2 to 4',labels,Vfwd,Vrvs,deltaV,points,hysteresis=True)
    