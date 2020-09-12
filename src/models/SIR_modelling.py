# importing python packages
import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import optimize
from scipy import integrate

#setting parameters for DataFrame
pd.set_option('display.max_rows', 500)

#importing data
df_raw = pd.read_csv('../data/raw/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
country_list = df_raw['Country/Region'].unique()
date = df_raw.columns[4:]
df_final = pd.DataFrame({'Date': date})

#transforming the raw data to accessible for SIR model
for each in country_list:
    df_final[each] = np.array(df_raw[df_raw['Country/Region'] == each].iloc[:,4::].sum(axis=0)).T
    
df_final.to_csv("../data/raw/COVID-19/csse_covid_19_data/SIR_modelling.csv", sep = ';', index=False)

df_analyse=pd.read_csv('../data/raw/COVID-19/csse_covid_19_data/SIR_modelling.csv',sep=';')

df_analyse.sort_values('Date',ascending=True).head()


# Intialize parameter
N0 = 1000000
beta = 0.4
gamma = 0.1
I0=df_analyse.Germany[35]
S0=N0-I0
R0=0

df_data = df_analyse[35:]
t = np.arange(df_data.shape[0])

def SIR_model_t(SIR,t,beta,gamma):
    ''' Simple SIR model
        S: susceptible population
        t: time step, mandatory for integral.odeint
        I: infected people
        R: recovered people
        beta: 
        
        overall condition is that the sum of changes (differnces) sum up to 0
        dS+dI+dR=0
        S+I+R= N (constant size of population)
    
    '''
    
    S,I,R=SIR
    dS_dt=-beta*S*I/N0          #S*I is the 
    dI_dt=beta*S*I/N0-gamma*I
    dR_dt=gamma*I
    return dS_dt,dI_dt,dR_dt
    
def fit_odeint(x, beta, gamma):
    '''
    helper function for the integration
    '''
    return integrate.odeint(SIR_model_t, (S0, I0, R0), t, args=(beta, gamma))[:,1] # we only would like to get dI

#calculating optimize parameters for every country
for country in df_data.columns[1:]:
    
        # preparing ydata so that, SIR modellig starts when the cases are greater than 0, for every country
        
        ydata = np.array(df_data[df_data[country]>0][country]) 
        t = np.arange(len(ydata))
        I0=ydata[0]
        S0=N0-I0
        R0=0
        popt=[0.4,0.1]
        fit_odeint(t, *popt)
        popt, pcov = optimize.curve_fit(fit_odeint, t, ydata, maxfev=5000)
        perr = np.sqrt(np.diag(pcov))
        fitted=fit_odeint(t, *popt)
        fit_pad = np.concatenate((np.zeros(df_data.shape[0]-len(fitted)) ,fitted))
        df_data[country + '_fitted'] = fit_pad

df_data = df_data.reset_index(drop=True)
df_data.to_csv('../data/processed/SIR_fitted.csv', sep = ';')


