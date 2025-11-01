#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 10:03:04 2025

@author: pierre
"""

from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
from graph_functions import question_info,question_histogramme,question_multiple_histogramme,categorie_info,panel_content,commentaires
import dash_bootstrap_components as dbc

# Chargement des données et conversion des notes en entier
df = pd.read_csv('./data/EPCI_2025/reponses-epci-200023414.csv')
for q in ['q2','q3','q6','q7','q8','q9','q10','q11','q12','q13','q14','q15',
          'q16','q17','q18','q19','q20','q21','q22','q23','q24','q25','q26',
          'q27','q28','q29','q30','q31','q32','q33','q37','q39','q41',
          'q42','q43','q44','q45','q46','q47','q48','q50','q52','q53','q54',
          'q55','q56','q57','q65']:
    try:
        df[q] = df[q].astype('Int64')
    except:
        print(q)

# Extraction des données de Seine-Maritime et intégration des noms de communes
communes = pd.read_csv('./data/EPCI_2025/communes_2024.csv')
communes=communes.loc[communes['DEP']=='76']
communes = communes[['COM','LIBELLE']]
communes['COM']=communes['COM'].astype(int)
communes=communes.rename(columns={'COM':'insee','LIBELLE':'commune'})
df = df.merge(communes, how='inner', on='insee')

# Panneau de filtrage des données
villes=sorted(list(df['commune'].unique()))
selection_pane = dbc.Offcanvas([
    dbc.Row([
        dbc.Col([
            html.Fieldset([
                html.Legend('Genre'),
                dcc.Checklist([
                    {'label':'Féminin', 'value':1},
                    {'label':'Masculin', 'value':2},
                    {'label':'Ne se prononce pas', 'value':3}],
                    value=[1,2,3],id='genre_selection')
                ]),
            html.Fieldset([
                html.Legend("Niveau d'expertise déclaré"),
                dcc.Checklist([
                    {'label':'1 - Débutant·e', 'value':1},
                    {'label':'2', 'value':2},
                    {'label':'3', 'value':3},
                    {'label':'4', 'value':4},
                    {'label':'5', 'value':5},
                    {'label':'6 - Expert·e', 'value':6}],
                    value=[1,2,3,4,5,6],
                    id='expertise_selection'
                    )
                ]),
            html.Fieldset([
                html.Legend("Pratiquant"),
                dcc.Checklist([
                    {'label':'Cycliste', 'value':1},
                    {'label':'Non cycliste', 'value':2}],
                    value=[1,2],
                    id='pratiquant_selection'
                    )
                ])
            ]),
        dbc.Col([
            html.Fieldset([
                html.Legend("Tranche d'âge"),
                dcc.Checklist([
                    {'label':'Moins de 11 ans', 'value':0},
                    {'label':'11 - 14 ans', 'value':1},
                    {'label':'15 - 18 ans', 'value':2},
                    {'label':'19 - 24 ans', 'value':3},
                    {'label':'25 - 34 ans', 'value':4},
                    {'label':'35 - 44 ans', 'value':5},
                    {'label':'45 - 54 ans', 'value':6},
                    {'label':'55 - 64 ans', 'value':7},
                    {'label':'65 - 75 ans', 'value':8},
                    {'label':'Plus de 75 ans', 'value':9},
                    {'label':'Ne se prononce pas', 'value':10}],
                    value=[0,1,2,3,4,5,6,7,8,9,10],
                    id='age_selection')
                ])
            ])
        ])
    ],
    id="offcanvas",
    title="Filtre",
    is_open=False
    )

# Panneau de synthèse (A enrichir)
synthese_pane = [
    html.Div([
        #html.H2('Evaluation globale de ')
        html.P(['Nombre de réponses : ',html.A(id='nb_rep')]),
        html.P(['Nombre de réponses valides : ',html.A(id='nb_val_rep')]),
        html.P(['Nombre de réponses de cyclistes : ',html.A(id='nb_rep_cyclist')]),
        #html.H3(['Evaluation globale : ' ])
        ])
    ]

# Panneaux des catégories
categories = {'ressenti':['q8','q9','q10','q11','q12','q13'],
              'securite':['q14','q15','q16','q17','q18','q19'],
              'confort':['q20','q21','q22','q23','q24'],
              'efforts':['q25','q26','q27','q28'],
              'services':['q29','q30','q31','q32']
              }

ressenti_pane = panel_content('ressenti',['q8','q9','q10','q11','q12','q13'])
securite_pane = panel_content('securite',['q14','q15','q16','q17','q18','q19'])
confort_pane = panel_content('confort',['q20','q21','q22','q23','q24'])
effort_pane = panel_content('efforts',['q25','q26','q27','q28'])
stationnement_pane = panel_content('services',['q29','q30','q31','q32'])

# Panneaux complémentaires

resume_pane = dbc.Container()

sociologie_pane = dbc.Container(dbc.Row([
    dbc.Col([
        html.H3('Répondant·e·s cyclistes'),
        html.Div(dcc.Graph(id='age_cyclistes')),
        html.Div(dcc.Graph(id='genre_cyclistes')),
        html.Div(dcc.Graph(id='expertise_cyclistes')),
        html.Div(dcc.Graph(id='permis_cyclistes')),
        html.Div(dcc.Graph(id='motorise_cyclistes')),
        html.Div(dcc.Graph(id='TEC_cyclistes')),
        html.Div(dcc.Graph(id='velo_cyclistes')),
        html.Div(dcc.Graph(id='motif_cyclistes')),
        html.Div(dcc.Graph(id='association_cyclistes')),
        html.Div(dcc.Graph(id='stationnement_cyclistes')),
        html.Div(dcc.Graph(id='vol_cyclistes')),
        ]),
    dbc.Col([
        html.H3('Répondant·e·s non cyclistes'),
        html.Div(dcc.Graph(id='age_non_cyclistes')),
        html.Div(dcc.Graph(id='genre_non_cyclistes')),
        html.Div(dcc.Graph(id='expertise_non_cyclistes')),
        html.Div(dcc.Graph(id='permis_non_cyclistes')),
        html.Div(dcc.Graph(id='motorise_non_cyclistes')),
        html.Div(dcc.Graph(id='TEC_non_cyclistes')),
        html.Div(dcc.Graph(id='mobilite_non_cyclistes')),
        html.Div(dcc.Graph(id='motif_non_cyclistes')),
        html.Div(dcc.Graph(id='velo_non_cyclistes')),
        #Habiture de mobilité q49
        #Possède un vélo q50
        ])
    ]))

commentaires_pane = dbc.Container(dbc.ListGroup(id='commentaires'))

violence_pane = []

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# App layout
app.layout = html.Div([
    html.Div(dbc.Row([dbc.Col(dcc.Dropdown(villes,'Rouen',id='ville_selection')),
                     dbc.Col(dbc.Button('Filtrer',id='open-offcanvas',n_clicks=0))])),
    html.Div(selection_pane),
    dcc.Tabs([
        dcc.Tab(label='Synthèse', children = synthese_pane),
        dcc.Tab(label='Ressenti général', children = ressenti_pane),
        dcc.Tab(label='Sécurité', children = securite_pane),
        dcc.Tab(label='Confort', children = confort_pane),
        dcc.Tab(label='Efforts de la commune', children = effort_pane),
        dcc.Tab(label='Stationnements et services', children = stationnement_pane),
        dcc.Tab(label='Résumé', children = resume_pane),
        dcc.Tab(label='Commentaires', children = commentaires_pane),
        dcc.Tab(label='Sociologie et pratique', children = sociologie_pane),
        dcc.Tab(label='Violence motorisée', children = violence_pane)
    ])
])

io = [
    Output('nb_rep', 'children'),
    Output('nb_val_rep', 'children'),
    Output('nb_rep_cyclist', 'children')]

for c in categories:
    io.append(Output('note_'+c,'children'))
    io.append(Output('histogramme_'+c,'figure'))
    for q in categories[c]:
        io.append(Output('moyenne_'+q,'children'))
        io.append(Output('histogramme_'+q,'figure'))

io.extend([
    Output('age_cyclistes','figure'),
    Output('age_non_cyclistes','figure'),
    Output('genre_cyclistes','figure'),
    Output('genre_non_cyclistes','figure'),
    Output('expertise_cyclistes','figure'),
    Output('expertise_non_cyclistes','figure'),
    Output('permis_cyclistes','figure'),
    Output('permis_non_cyclistes','figure'),
    Output('motorise_cyclistes','figure'),
    Output('motorise_non_cyclistes','figure'),
    Output('TEC_cyclistes','figure'),
    Output('TEC_non_cyclistes','figure'),
    Output('velo_cyclistes','figure'),
    Output('association_cyclistes','figure'),
    Output('motif_cyclistes','figure'),
    Output('motif_non_cyclistes','figure'),
    Output('stationnement_cyclistes','figure'),
    Output('vol_cyclistes','figure'),
    Output('mobilite_non_cyclistes','figure'),
    Output('velo_non_cyclistes','figure')
    ])

io.append(Output('commentaires', 'children'))

io.extend([
    Input('ville_selection', 'value'),
    Input('genre_selection', 'value'),
    Input('expertise_selection', 'value'),
    Input('pratiquant_selection','value'),
    Input('age_selection','value')
    ])

@callback(tuple(io))
def update(ville,genre,expertise,pratique,age) :
    commune_selection = df['commune']==ville
    genre_selection = df['q47'].isin(genre) | df['q56'].isin(genre)
    expertise_selection = df['q37'].isin(expertise) | df['q52'].isin(expertise)
    age_selection = df['q48'].isin(age) | df['q57'].isin(age)
    pratique_selection = ((df['q6']<=4) & (1 in pratique)) | ((df['q6']==5) & (2 in pratique))
    
    selection = commune_selection & genre_selection & expertise_selection & age_selection & pratique_selection
    
    data = df.loc[selection]
    
    nb_rep = len(data)
    data = data.loc[data['commentaires'].isna()]
    nb_val_rep = len(data)
    cyclist_df = data.loc[df['q6']!=5]
    non_cyclist_df = data.loc[df['q6']==5]
    nb_rep_cyclist = len(cyclist_df)
    
    return_value = [nb_rep,nb_val_rep,nb_rep_cyclist]

    for c in categories:
        return_value.extend(categorie_info(data,c))
        for q in categories[c]:
            return_value.extend(question_info(data, q))
    
    return_value.append(question_histogramme(data,'q48'))
    return_value.append(question_histogramme(data,'q57'))
    return_value.append(question_histogramme(data,'q47'))
    return_value.append(question_histogramme(data,'q56'))
    return_value.append(question_histogramme(data,'q37'))
    return_value.append(question_histogramme(data,'q52'))
    return_value.append(question_histogramme(data,'q43'))
    return_value.append(question_histogramme(data,'q53'))
    return_value.append(question_histogramme(data,'q44'))
    return_value.append(question_histogramme(data,'q54'))
    return_value.append(question_histogramme(data,'q45'))
    return_value.append(question_histogramme(data,'q55'))
    return_value.append(question_multiple_histogramme(data,'q40'))
    return_value.append(question_histogramme(data,'q46'))
    return_value.append(question_multiple_histogramme(data,'q36'))
    return_value.append(question_multiple_histogramme(data,'q51'))
    return_value.append(question_histogramme(data,'q41'))
    return_value.append(question_histogramme(data,'q42'))
    return_value.append(question_multiple_histogramme(data,'q49'))
    return_value.append(question_histogramme(data,'q50'))

    return_value.append(commentaires(data))

    return tuple(return_value)

@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Run the app
if __name__ == '__main__':
    app.run(debug=False)