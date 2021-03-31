# Datenverarbeitung
import requests
import json
import pandas as pd

# Dashboard
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask

# Daten vom GovData-API abfragen
response = requests.get('https://www.govdata.de/ckan/api/3/action/organization_list?include_dataset_count=True&all_fields=True')
orgs = json.loads(response.text)['result']
dataset_counts = dict([(str(x['display_name']), int(x['package_count'])) for x in orgs]) # Zu Dictionary umformattieren

# Departments.json laden und einlesen
with open('departments.json', 'r', encoding='utf-8') as f:
    data = f.read()
deps = json.loads(data)['departments']

# Aus Dictionary Liste von Ministeriennamen lesen
def read_names(dept_dict):
    names = [dept_dict['name']]
    if "subordinates" in dept_dict:
        for x in dept_dict['subordinates']:
            names.append(x['name'])
    return names
names = [read_names(x) for x in deps]

# Durch Namen iterieren, um Long-Format Dataframe für Visualisierung zu kreieren
df_data = []
for amt in names:
    for branch in amt:
        if branch in dataset_counts:
            df_data.append([amt[0], branch, int(dataset_counts[branch])])
        else:
            df_data.append([amt[0], branch, 0]) # Auch Departments mit einbeziehen, die keine Datasets hochgeladen haben
df = pd.DataFrame(df_data, columns = ['Ministerium', 'Amt', 'Datensätze'])
df.sort_values(by = 'Datensätze', ascending = False, inplace = True)

# Visualisierung - Parameter sind hoffentlich selbsterklärend
fig = px.bar(df, x = 'Ministerium', 
       y = 'Datensätze', 
       color = 'Amt',
       text = 'Datensätze',
       hover_name = 'Amt',
       height = 768,
       width  = 1000
       )

fig.update_layout(
    showlegend = False, # Keine Legende
    updatemenus=[ # Toggle zwischen linearer und logarithmischer Y-Achse
            dict(
                 buttons=list([
                     dict(label="Linear",  
                          method="relayout", 
                          args=[{"yaxis.type": "linear"}]),
                     dict(label="Logarithmisch", 
                          method="relayout", 
                          args=[{"yaxis.type": "log"}]),
                                  ]),
            x = 1.3 , y = 1
            )])

# Figure to html
fig.write_html('plot.html')

# Dashboard kreieren und Server starten
layout = html.Div([
            html.Div(
                    [html.H1('GovData Dashboard')], 
                    style={'textAlign': 'center'}),
            html.Div(
                    [dcc.Graph(figure=fig)],
                    style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
        ])

server = Flask(__name__)
BS = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/litera/bootstrap.min.css'
app = dash.Dash(__name__,  server=server, external_stylesheets=[BS])
app.layout = layout
app.run_server(debug=True)