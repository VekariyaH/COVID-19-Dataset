import subprocess
import os

import pandas as pd
import numpy as np

from datetime import datetime

import requests
import json

def get_john_hopkins():
    git_pull = subprocess.Popen( "git pull",
                           cwd = os.path.dirname('C:/Users/hosha/applied_data_science_covid19/data/raw/COVID-19/' ),
                           shell = True,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE)
                           
    (out, error) = git_pull.communicate()

    print("Error : " + str(error))
    print("Out : " + str(out))
    
def get_current_data_germany():
    
    #16 states
    #data = requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')

    #400 regions/Landkreis
    
    data = requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')
    
    json_object = json.loads(data.content)
    full_list = []
    for pos,each_dict in enumerate (json_object['features'][:]):
        full_list.append(each_dict['attributes'])
        
    pd_full_list = pd.DataFrame(full_list)
    pd_full_list.to_csv('C:/Users/hosha/applied_data_science_covid19/data/raw/NPGEO/GER_state_data.csv',sep=';')
    print('Number of regions rows: '+str(pd_full_list.shape[0]))
    
if __name__ == '__main__':
    get_john_hopkins()
    get_current_data_germany()