# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:22:20 2021

@author: ayuso
"""

import os
import numpy as np
from scipy import stats
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
plt.rcParams.update({'font.size': 17})

fig_size = (15,10)
f = plt.figure(figsize=fig_size)

def plot_2TM_probestation(file_name,sample,fig=f,markers='',legend=''):
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

f=plot_2TM_probestation('I06_1RTA_contact3to4_1Vsd.csv', 'I06',f,'ro','1stRTA')

#plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))
#plt.ticklabel_format(axis='y',style='scientific',scilimits=(0,0))


fig_size = (15,10)
j = plt.figure(figsize=fig_size)

def LinReg_2TM_probestation(file_name,sample,Vfwd,Vrvs,deltaV,points,hysteresis=True):
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


(voltage_SD1,currentuA1,V_fwd,slope2Tfwd,intercept2Tfwd,V_rvs,slope2Trvs,intercept2Trvs) = LinReg_2TM_probestation('I06_2RTA_contact3to4_1Vsd_bis.csv','I06',1,-0.5,0.25,5,j,'ro','2rdRTA',hysteresis=True)

#plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))
#plt.ticklabel_format(axis='y',style='scientific',scilimits=(0,0))


#%%

def Plots_2TM_probestation(file_name,sample,Vfwd,Vrvs,deltaV,points,markers='',legend='',hysteresis=True):
    (voltage_SD1,currentuA1,V_fwd,slope2Tfwd,intercept2Tfwd,V_rvs,slope2Trvs,intercept2Trvs)=LinReg_2TM_probestation(file_name, sample, Vfwd, Vrvs, deltaV, points)
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


j = Plots_2TM_probestation('I06_2RTA_contact3to4_1Vsd_bis.csv','I06',1,-0.5,0.25,5,'ro','2rdRTA',hysteresis=True)
#plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))
#plt.ticklabel_format(axis='y',style='scientific',scilimits=(0,0))


#%% Diff resistance

def diff_resistance(file_name,sample,fig=f,markers='',legend=''):
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
h = diff_resistance('I06_1RTA_contact3to4_1Vsd.csv', 'I06',h,'r-','1stRTA')
