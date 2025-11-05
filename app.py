#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 10:03:04 2025

@author: pierre
"""

from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
from graph_functions import question_info, question_histogramme
from graph_functions import question_multiple_histogramme, categorie_info
from graph_functions import panel_content, commentaires, note
from graph_functions import progress, evolution
import dash_bootstrap_components as dbc

# Chargement des données et conversion des notes en entier
df = pd.read_csv('./data/EPCI_2025/reponses-epci-242900314.csv')
for q in ['q2', 'q3', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13',
          'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22', 'q23',
          'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30', 'q31', 'q32', 'q33',
          'q37', 'q39', 'q41', 'q42', 'q43', 'q44', 'q45', 'q46', 'q47', 'q48',
          'q50', 'q52', 'q53', 'q54', 'q55', 'q56', 'q57', 'q65']:
    df[q] = df[q].astype('Int64')

categories = {'ressenti': ['q8', 'q9', 'q10', 'q11', 'q12', 'q13'],
              'securite': ['q14', 'q15', 'q16', 'q17', 'q18', 'q19'],
              'confort': ['q20', 'q21', 'q22', 'q23', 'q24'],
              'efforts': ['q25', 'q26', 'q27', 'q28'],
              'services': ['q29', 'q30', 'q31', 'q32']
              }

for c in categories:
    df[c.upper()] = sum([df[col] 
                         for col in categories[c]]) / len(categories[c])

df['NOTE'] = sum([df[c.upper()] for c in categories]) / len(categories)

# Extraction des données de Seine-Maritime et intégration des noms de communes
communes = pd.read_csv('./data/EPCI_2025/communes_2024.csv')
communes = communes.loc[communes['DEP'] == '29']
communes = communes[['COM', 'LIBELLE']]
communes['COM'] = communes['COM'].astype(int)
communes = communes.rename(columns={'COM': 'insee', 'LIBELLE': 'commune'})
df = df.merge(communes, how='inner', on='insee')

# Panneau de filtrage des données
villes = ['Toutes les communes']+sorted(list(df['commune'].unique()))
selection_pane = dbc.Offcanvas([
    dbc.Row([
        dbc.Col([
            html.Fieldset([
                html.Legend('Genre'),
                dbc.Checklist([
                    {'label': 'Féminin', 'value': 1},
                    {'label': 'Masculin', 'value': 2},
                    {'label': 'Ne se prononce pas', 'value': 3}],
                    value=[1, 2, 3], id='genre_selection', switch=True)
                ]),
            html.Fieldset([
                html.Legend("Niveau d'expertise déclaré"),
                dbc.Checklist([
                    {'label': '1 - Débutant·e', 'value': 1},
                    {'label': '2', 'value': 2},
                    {'label': '3', 'value': 3},
                    {'label': '4', 'value': 4},
                    {'label': '5', 'value': 5},
                    {'label': '6 - Expert·e', 'value': 6}],
                    value=[1, 2, 3, 4, 5, 6],
                    id='expertise_selection', switch=True
                    )
                ]),
            html.Fieldset([
                html.Legend("Pratiquant"),
                dbc.Checklist([
                    {'label': 'Cycliste', 'value': 1},
                    {'label': 'Non cycliste', 'value': 2}],
                    value=[1, 2],
                    id='pratiquant_selection', switch=True
                    )
                ])
            ]),
        dbc.Col([
            html.Fieldset([
                html.Legend("Tranche d'âge"),
                dbc.Checklist([
                    {'label': 'Moins de 11 ans', 'value': 0},
                    {'label': '11 - 14 ans', 'value': 1},
                    {'label': '15 - 18 ans', 'value': 2},
                    {'label': '19 - 24 ans', 'value': 3},
                    {'label': '25 - 34 ans', 'value': 4},
                    {'label': '35 - 44 ans', 'value': 5},
                    {'label': '45 - 54 ans', 'value': 6},
                    {'label': '55 - 64 ans', 'value': 7},
                    {'label': '65 - 75 ans', 'value': 8},
                    {'label': 'Plus de 75 ans', 'value': 9},
                    {'label': 'Ne se prononce pas', 'value': 10}],
                    value=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    id='age_selection', switch=True)
                ])
            ])
        ])
    ],
    id="offcanvas",
    title="Filtre",
    is_open=False
    )

# Panneau de présentation
presentation_pane = html.Div(dbc.Container([
    html.H1(["Résultats du Baromètre Vélo 2025 ",
             "sur Brest métropole"]),
    html.H2('Présentation'),
    html.P(["Le ",
            html.A("baromètre vélo", href="https://www.barometre-velo.fr/"),
            " est une grande enquête citoyenne organisée à l'échelle ",
            "nationale par la ",
            html.A("Fédération des Usagères et Usagers de la Bicylette (FUB)",
                   href="https://www.fub.fr/"),
            ". Elle vise à recueillir l'appréciation des répondants sur les ",
            "conditions de pratique du vélo à l'échelle des communes. ",
            "La méthodologie de l'enquête et ses résultats sont présentés ",
            "sur le site du baromètre.",
            ]),
    html.P(["Ce site a pour vocation d'offrir des outils permettant une ",
            "analyse fine des résultats du baromètre vélo ",
            "sur le territoire de ",
            html.A("Brest métropole",
                   href="https://brest.fr/"),
            ". Outre les résultats déjà disponibles sur le site du ",
            "baromètre, ce site permet : ",
            html.Ul([
                html.Li(["d'analyser les résultats pour ",
                         "les communes non classées"]),
                html.Li(["d'analyser les résultats en fonction du profil ",
                         "des répondants"]),
                html.Li("d'analyser les données sociologiques des répondants"),
                html.Li(["d'analyser les caractéristiques de pratique ",
                         "du vélo des répondants"]),
                html.Li(["d'analyser le rapport des répondants aux autres ",
                         "modes de déplacements"]),
                html.Li(["de consulter les commentaires textuels déposés ",
                         "sur les contributions individuelles"])
                ])
            ]),
    html.P(["Ce site exploite les données des contributions individuelles ",
            "recueillies lors de l'enquête et mises à disposition sur la ",
            html.A("plateforme Opendata de la FUB",
                   href="https://opendata.parlons-velo.fr/"),
            ". Ces données sont anonymes et conformes au RGPD."
            ]),
    html.P(["Ce site est une copie de l'outil développé par Pierre Héroux pour le compte ",
            "de l'association ",
            html.A("SABINE", href="sabinerouenvelo.org"),
            " qui promeut l'usage du vélo comme moyen de déplacement sur le ",
            "territoire de la Métropole Rouen Normandie. ",
            "Son code source est disponible sur ",
            html.A("https://github.com/PierreHeroux/BarometreVeloMRN2025",
                   href="https://github.com/PierreHeroux/BarometreVeloMRN2025"),
            " sous licence GPL3.0"
            ]),
    html.P(["La version brestoise est gérée par l'association ",
            html.A("Brest à Pied et à Vélo (BaPaV)",
                   href="https://www.bapav.org/"),
            "."
            ]),
    html.H2("Mode d'emploi"),
    html.P(["Sélectionnez la commune à analyser dans la liste déroulante. ",
            "Le bouton ",
            dbc.Button("Filtrer", id='open-offcanvas-2', n_clicks=0),
            " vous permet de restreindre l'analyse à certains profils ",
            "de répondants."]),
    html.P("Les différents onglets présentent diverses analyses."),
    html.Ul([
        html.Li(["L'onglet Synthèse présente une analyse globale ",
                 "des résultats."]),
        html.Li(["Les onglets 'Ressenti général', 'Sécurité', 'Confort', ",
                 "'Efforts de la commune' et 'Stationnements et services' ",
                 "présentent chancun une analyse pour ces catégories de ",
                 "questions ainsi qu'une analyse de chacun des questions ",
                 "dans le détail."]),
        html.Li(["L'onglet 'Commentaires' liste l'ensemble des commentaires ",
                 "textuels additionnels déposés par les répondants."]),
        html.Li(["L'onglet 'Sociologie et pratique' donne une analyse des ",
                 "données sociologiques des répondants en distinguant les ",
                 "cyclistes et les non cyclistes. Il présente également des ",
                 "analyses relatives à la pratique du vélo et au rapport aux ",
                 "autres modes de déplacement."])
        ])
    ]))

# Panneau de synthèse (A enrichir)
row1 = html.Tr([html.Td("Nombre total de réponses"),
                html.Td(html.A(id='nb_rep'))])
row2 = html.Tr([html.Td("Nombre de réponses valides"),
                html.Td(html.A(id='nb_val_rep'))])
row3 = html.Tr([html.Td("Nombre de réponses de cyclistes"),
                html.Td(html.A(id='nb_rep_cyclist'))])


synthese_pane = dbc.Container(
    html.Div([
        html.H1(["Synthèse de l'évaluation donnée par le baromètre vélo pour ",
                 html.Span(id='commune')]),
        html.H2('Evaluation globale'),
        html.Span(id='note'),
        html.H2('Ressenti général'),
        html.Span(id='ressenti'),
        html.H2('Sécurité'),
        html.Span(id='securité'),
        html.H2('Confort'),
        html.Span(id='confort'),
        html.H2('Efforts de la commune'),
        html.Span(id='efforts'),
        html.H2('Stationnement et services'),
        html.Span(id='stationnement'),
        html.H2('Evolution depuis 2 ans'),
        html.Span(id='evolution'),
        html.H2('Nombre de réponses'),
        dbc.Table(html.Tbody([row1, row2, row3]))
        ])
    )

# Panneaux des catégories

ressenti_pane = panel_content('ressenti',
                              ['q8', 'q9', 'q10', 'q11', 'q12', 'q13'])
securite_pane = panel_content('securite',
                              ['q14', 'q15', 'q16', 'q17', 'q18', 'q19'])
confort_pane = panel_content('confort',
                             ['q20', 'q21', 'q22', 'q23', 'q24'])
effort_pane = panel_content('efforts',
                            ['q25', 'q26', 'q27', 'q28'])
stationnement_pane = panel_content('services',
                                   ['q29', 'q30', 'q31', 'q32'])

# Panneaux complémentaires

sociologie_pane = dbc.Card(dbc.CardBody(dbc.Row([
    dbc.Col(html.Div([
        html.H2('Répondant·e·s cyclistes'),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='age_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='genre_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='expertise_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='permis_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='motorise_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='TEC_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='velo_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='motif_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='association_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='stationnement_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='vol_cyclistes')),
        ], className="h-100 p-5 text-white bg-primary rounded-3")),
    dbc.Col(html.Div([
        html.H2('Répondant·e·s non cyclistes'),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='age_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='genre_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='expertise_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='permis_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='motorise_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='TEC_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='mobilite_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='motif_non_cyclistes')),
        html.Hr(className="my-2"),
        html.Div(dcc.Graph(id='velo_non_cyclistes')),
        ], className="h-100 p-5 text-white bg-primary rounded-3"))
    ])), className="mt-3")

commentaires_pane = dbc.Container(html.Div([
    html.H2("Commentaires en texte libre", className="display-3"),
    html.Hr(className="my-2"),
    dbc.ListGroup(id='commentaires')],
    className="h-100 p-5 text-white bg-primary rounded-3"))

violence_pane = dbc.Container(html.Div([
    html.H2("Violences motorisées", className="display-3"),
    html.Hr(className="my-2"),
    dcc.Graph(id='situations_violence'),
    html.Hr(className="my-2"),
    dcc.Graph(id='plaintes'),
    html.Hr(className="my-2"),
    dcc.Graph(id='suites_plaintes'),
    ], className="h-100 p-5 text-white bg-primary rounded-3"))

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.title = 'Baromètre Vélo 2025 Brest métropole'

# App layout
options = [{'label': v, 'value': v} for v in villes]
app.layout = html.Div([
    dbc.Row([dbc.Col(dbc.Select(options=options,
                                id='ville_selection',
                                value='Toutes les communes')),
             dbc.Col(dbc.Button('Filtrer',
                                id='open-offcanvas',
                                n_clicks=0))]),
    html.Div(selection_pane),
    dcc.Loading(id="loading",
                type='default',
                children=html.Div(id="loading-output")),
    dbc.Tabs([
        dbc.Tab(label="Présentation", children=presentation_pane),
        dbc.Tab(label='Synthèse', children=synthese_pane),
        dbc.Tab(label='Ressenti général', children=ressenti_pane),
        dbc.Tab(label='Sécurité', children=securite_pane),
        dbc.Tab(label='Confort', children=confort_pane),
        dbc.Tab(label='Efforts de la commune', children=effort_pane),
        dbc.Tab(label='Stationnements et services',
                children=stationnement_pane),
        dbc.Tab(label='Commentaires', children=commentaires_pane),
        dbc.Tab(label='Sociologie et pratique', children=sociologie_pane),
        dbc.Tab(label='Violence motorisée', children=violence_pane)
    ])
])

io = [
      Output('commune', 'children'),
      Output('note', 'children'),
      Output('ressenti', 'children'),
      Output('securité', 'children'),
      Output('confort', 'children'),
      Output('efforts', 'children'),
      Output('stationnement', 'children'),
      Output('evolution', 'children'),
      Output('nb_rep', 'children'),
      Output('nb_val_rep', 'children'),
      Output('nb_rep_cyclist', 'children')]

for c in categories:
    io.append(Output('note_' + c, 'children'))
    io.append(Output('histogramme_' + c, 'figure'))
    for q in categories[c]:
        io.append(Output('moyenne_' + q, 'children'))
        io.append(Output('histogramme_' + q, 'figure'))

io.extend([
    Output('age_cyclistes', 'figure'),
    Output('age_non_cyclistes', 'figure'),
    Output('genre_cyclistes', 'figure'),
    Output('genre_non_cyclistes', 'figure'),
    Output('expertise_cyclistes', 'figure'),
    Output('expertise_non_cyclistes', 'figure'),
    Output('permis_cyclistes', 'figure'),
    Output('permis_non_cyclistes', 'figure'),
    Output('motorise_cyclistes', 'figure'),
    Output('motorise_non_cyclistes', 'figure'),
    Output('TEC_cyclistes', 'figure'),
    Output('TEC_non_cyclistes', 'figure'),
    Output('velo_cyclistes', 'figure'),
    Output('association_cyclistes', 'figure'),
    Output('motif_cyclistes', 'figure'),
    Output('motif_non_cyclistes', 'figure'),
    Output('stationnement_cyclistes', 'figure'),
    Output('vol_cyclistes', 'figure'),
    Output('mobilite_non_cyclistes', 'figure'),
    Output('velo_non_cyclistes', 'figure'),
    Output('situations_violence', 'figure'),
    Output('plaintes', 'figure'),
    Output('suites_plaintes', 'figure')
    ])

io.append(Output('commentaires', 'children'))
io.append(Output("loading-output", "children"))

io.extend([
    Input('ville_selection', 'value'),
    Input('genre_selection', 'value'),
    Input('expertise_selection', 'value'),
    Input('pratiquant_selection', 'value'),
    Input('age_selection', 'value')
    ])


@callback(tuple(io))
def update(commune, genre, expertise, pratique, age):
    """
    Permet la mise à jour des champs variables.

    A chaque interaction sur les champs Inout, cette fonction est appelée. Elle
    permet la mise à jour des champs variables.

    Parameters
    ----------
    commune : str
        Châine de caractère représentant la commune.
    genre : list
        Liste d'entiers représentant les genres des répondants dont les
        réponses sont analysées.
    expertise : list
        Liste d'entiers représentant les niveaux d'expertise des répondants
        dont les réponses sont analysées.
    pratique : list
        Liste d'entiers représentant les cyclistes et non-cyclistes.
    age : list
        Liste d'entiers représentants les différentes catégories d'âges des
        répondants dont les réponses sont retenues pour analyse

    Returns
    -------
    tuple
        Tuple composé des différentes valeurs pour les champs variables.

    """
    genre_selection = df['q47'].isin(genre) | df['q56'].isin(genre)
    expertise_selection = df['q37'].isin(expertise) | df['q52'].isin(expertise)
    age_selection = df['q48'].isin(age) | df['q57'].isin(age)
    pratique_selection = ((df['q6'] <= 4) & (1 in pratique)) \
        | ((df['q6'] == 5) & (2 in pratique))

    if commune == 'Toutes les communes':
        selection = genre_selection & expertise_selection \
            & age_selection & pratique_selection
    else:
        commune_selection = df['commune'] == commune
        selection = commune_selection & genre_selection & expertise_selection \
            & age_selection & pratique_selection
    data = df.loc[selection]
    nb_rep = len(data)
    data = data.loc[data['commentaires'].isna()]
    nb_val_rep = len(data)
    cyclist_df = data.loc[df['q6'] != 5]
    nb_rep_cyclist = len(cyclist_df)
    return_value = [commune,
                    progress(note(data, 'NOTE')),
                    progress(note(data, 'ressenti'.upper())),
                    progress(note(data, 'securite'.upper())),
                    progress(note(data, 'confort'.upper())),
                    progress(note(data, 'efforts'.upper())),
                    progress(note(data, 'services'.upper())),
                    evolution(data),
                    nb_rep,
                    nb_val_rep,
                    nb_rep_cyclist]

    for c in categories:
        return_value.extend(categorie_info(data, c))
        for q in categories[c]:
            return_value.extend(question_info(data, q))
    return_value.append(question_histogramme(data, 'q48'))
    return_value.append(question_histogramme(data, 'q57'))
    return_value.append(question_histogramme(data, 'q47'))
    return_value.append(question_histogramme(data, 'q56'))
    return_value.append(question_histogramme(data, 'q37'))
    return_value.append(question_histogramme(data, 'q52'))
    return_value.append(question_histogramme(data, 'q43'))
    return_value.append(question_histogramme(data, 'q53'))
    return_value.append(question_histogramme(data, 'q44'))
    return_value.append(question_histogramme(data, 'q54'))
    return_value.append(question_histogramme(data, 'q45'))
    return_value.append(question_histogramme(data, 'q55'))
    return_value.append(question_multiple_histogramme(data, 'q40'))
    return_value.append(question_histogramme(data, 'q46'))
    return_value.append(question_multiple_histogramme(data, 'q36'))
    return_value.append(question_multiple_histogramme(data, 'q51'))
    return_value.append(question_histogramme(data, 'q41'))
    return_value.append(question_histogramme(data, 'q42'))
    return_value.append(question_multiple_histogramme(data, 'q49'))
    return_value.append(question_histogramme(data, 'q50'))
    return_value.append(question_multiple_histogramme(data, 'q38')),
    return_value.append(question_histogramme(data, 'q39')),
    return_value.append(question_histogramme(data, 'q62')),

    return_value.append(commentaires(data))
    return_value.append(None)

    return tuple(return_value)


@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    Input("open-offcanvas-2", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, n2, is_open):
    """
    Permet l'ouverture ou la fermeture du panneau de sélection.

    Parameters
    ----------
    n1 : int
        Valeur du bouton n1.
    n2 : int
        Valeur du bouton n2.
    is_open : bool
        Valeur d'ouverture du panneau de sélection.

    Returns
    -------
    bool
        Renvoie la valeur d'ouverture du panneau de sélection.

    """
    if n1 | n2:
        return not is_open
    return is_open


# Run the app
if __name__ == '__main__':
    app.run(debug=False)
