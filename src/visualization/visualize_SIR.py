# importing python packages
import os
import pandas as pd
import numpy as np
from datetime import datetime

import random

import plotly.graph_objects as go
import dash
print('Your current dash board version is:' + dash.__version__)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State

#importing data frame
df_analyse=pd.read_csv('../data/processed/SIR_fitted.csv',sep=';')
df_analyse.sort_values('Date',ascending=True).head()
df_analyse = df_analyse.reset_index(drop = True)
df_data = df_analyse[35:] #Need to be careful here because it difffers from each country!!

# for showing same color for each countries both curve, and color will be random at when you update the color list
color_list = []
for i in range(200):
    var = '#%02x%02x%02x'%(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    color_list.append(var)

# creating dashboard app containig plotting for whole dataset
fig = go.Figure()
app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    #  Applied Data Science on COVID-19 data - Dash Board 2
    
    - The default layout
        * Y-axis shows the confirmed infected cases in log-scale
        * X-axis shows the timeline in days
    
    - With the dropdown menu, user can visualize the curves for multiple countries

    - There are two plots in the dash board for each country:
    
    1. Plot of confirmed infected cases with respect to timeline.
    2. Plot of SIR curve respect to timeline. 
    
    '''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),
    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_data.columns[1:200]],
        value=['Germany','India'], # which are pre-selected
        multi=True),dcc.Graph(figure=fig, id='main_window_slope')])

@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value')])
def update_figure(country_list):
    
    my_yaxis={'type':"log",'title':'Confirmed infected people (From johns hopkins csse, log-scale)'}
    traces = []
    
    x = 0
    for each in country_list:
        traces.append(dict(x=df_data['Date'],y=df_data[each],
                                mode='line', line = dict(color = color_list[x]), opacity=1.0,name=each))
        traces.append(dict(x=df_data['Date'],
                                y=df_data[each+'_fitted'],
                                mode='markers+lines',line = dict(color=color_list[x]), opacity=1.0,name=each+'_simulated'))
        x = x+1

    return {
            'data': traces,
            'layout': dict (
                width=1000,height=650,
                xaxis={'title':'Timeline in Days','tickangle':-45,'nticks':20,
                'tickfont':dict(size=14,color="#0c6887"),},yaxis=my_yaxis)}

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)