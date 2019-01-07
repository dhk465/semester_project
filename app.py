import dash
import dash_core_components as dcc
import dash_html_components as html

import numpy as np
import pandas as pd
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go

# declaring a DataFrame from csv
aasd = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/MASS/Aids2.csv',
                   index_col=False)
# renaming the columns
aasd.rename({'diag': 'date of diagnosis',
             'death': 'date of death',
             'T.categ': 'mode of transmission',
             'age': 'age at diagnosis'},
            axis='columns', inplace=True)
# deleting the duplicate index numbers within csv
del aasd['Unnamed: 0']
# de-abbreviate the terms e.g. "D" into "Deceased" and "hs" into "male homosexual or bisexual contact"
# aasd['state'].unique()
deabbr_state = {'NSW': 'New South Wales',
                'Other': 'Others',
                'QLD': 'Queensland',
                'VIC': 'Victoria'}
aasd['state'] = aasd['state'].map(deabbr_state)
# aasd['status'].unique()
deabbr_status = {'A': 'alive',
                 'D': 'deceased'}
aasd['status'] = aasd['status'].map(deabbr_status)
# aasd['mode of transmission'].unique()
deabbr_mode = {'hs': 'male homosexual/bisexual contact',
               'haem': 'haemophilia/coagulation disorder', 
               'other': 'other/unknown', 
               'hsid': 'male homosexual/bisexual intravenous drug user', 
               'het': 'heterosexual contact', 
               'id': 'female or heterosexual male intravenous drug user', 
               'mother': 'mother with or at risk of HIV infection',
               'blood': 'receipt of blood, blood components or tissue'}
aasd['mode of transmission'] = aasd['mode of transmission'].map(deabbr_mode)
# add a new column based on the calculation date of death - date of diagnosis
aasd['days after diagnosis'] = aasd['date of death'].values - aasd['date of diagnosis'].values
# rearranging the columns
aasd = aasd[['state', 'sex', 'date of diagnosis', 'date of death', 'days after diagnosis', 'status', 'mode of transmission', 'age at diagnosis']]
# the number of the deceased during the study
aasd_alive = aasd[aasd['status'] == 'alive']
num_dec = len(aasd) - len(aasd_alive)
# the deceased participants at the end of the study are listed
# apart from these participants, the date of death value 11504 indicates the participants are alive as of the end of the study
last_day_dec = aasd[(aasd['date of death'] == 11504) & (aasd['status'] == 'deceased')]
male_stat = aasd[aasd['sex'] == 'M']
female_stat = aasd[aasd['sex'] == 'F']

# hist_age
hist01 = [go.Histogram(x=aasd['age at diagnosis'])]
layout01 = go.Layout(
    showlegend = True,
    height = 800,
    width = 1200,
    title = 'Age Distribution'
)

app = dash.Dash()

app.layout = html.Div(children=[

    html.H1(
        children='Python Semester Project'
    ),
    html.Div(children='''
        AIDS statistics in Australia up to 1992
    '''),    
    dcc.Dropdown(
    id='',
    options=[
        {'label': 'Raw Data', 'value': 'data'},
        {'label': 'Graphs', 'value': 'graph'}
    ],
    value='graph'
    ),

    html.Div(children=[
        dcc.Graph(
            id='hist_age',
            figure=dict(data = hist01, layout = layout01)
        )
    ])
])
    
if __name__ == '__main__':
    app.run_server()