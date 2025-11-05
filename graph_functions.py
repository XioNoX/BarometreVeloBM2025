#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 18:26:01 2025

@author: pierre
"""

import plotly.express as px
import dash_bootstrap_components as dbc
import json
from dash import html, dcc

questions = dict()
with open('./questions.json', 'r') as fd:
    questions = json.load(fd)

color = {'A+': 'rgb(43,121,16)',
         'A': 'rgb(75,152,51)',
         'B': 'rgb(121,181,45)',
         'C': 'rgb(200,210,39)',
         'D': 'rgb(254,239,48)',
         'E': 'rgb(252,203,44)',
         'F': 'rgb(243,153,57)',
         'G': 'rgb(228,55,35)'}

label = {'ressenti': 'Ressenti général',
         'securite': 'Sécurité',
         'confort': 'Confort',
         'efforts': 'Efforts de la commune',
         'services': 'Stationnements et services'
         }


def note(data, question):
    """
    Renvoie la moyenne à la question.

    Parameters
    ----------
    data : pandas.DataFrame
        Données à la base du calcul.
    question : str
        Nom de la question.

    Returns
    -------
    float
        Moyenne de la question sur les données.

    """
    return round(data[question].mean(), 2)


def classe_couleur(note):
    """
    Renvoie la classe et la couleur associée pour une note.

    Parameters
    ----------
    note : float
        Note.

    Returns
    -------
    classe : str
        Chaine de caractères définissante la classe de la note.
    couleur : str
        Chaine de caractères définissant la couleur de la note.

    """
    if note > 4.6:
        classe = 'A+'
    elif note > 4.3:
        classe = 'A'
    elif note > 3.9:
        classe = 'B'
    elif note > 3.5:
        classe = 'C'
    elif note > 3.1:
        classe = 'D'
    elif note > 2.7:
        classe = 'E'
    elif note > 2.3:
        classe = 'F'
    else:
        classe = 'G'
    couleur = color[classe]
    return classe, couleur


def badge(note):
    """
    Revoie un badge avec la note et la couleur.

    Parameters
    ----------
    note : float
        Valeur pour laquelle le badge est créé.

    Returns
    -------
    badge : dash_bootstrap_components.Badge
        Badge contenant la note moyenne de la colonne et dont la couleur est
        adaptée.

    """
    classe, couleur = classe_couleur(note)
    badge = dbc.Badge(classe+f' : {note:.2f}', color=couleur)
    return badge


def progress(note):
    """
    Renvoie une barre de progression représentant la note.

    Parameters
    ----------
    note : float
        Note à représenter.

    Returns
    -------
    progress : ash_bootstrap_components.Progress
        Barre de progression représentant la note

    """
    classe, couleur = classe_couleur(note)
    progress = dbc.Progress(label=classe+f' : {note:.2f}',
                            value=int(note/6*100),
                            color=couleur,
                            style={"height": "50px",
                                   "font-size": "30px",
                                   "text-shadow": "3px 3px #558abb"})
    return progress


def evolution(data):
    m = data['q7'].mean()-3
    if m > 0:
        content = [
            dbc.Progress(value=50, color='secondary', bar=True),
            dbc.Progress(value=m/2*50, color="success", bar=True),
            dbc.Progress(value=50-m/2*50, color='secondary', bar=True)
            ]
    else:
        content = [
            dbc.Progress(value=50+m/2*50, color='secondary', bar=True),
            dbc.Progress(value=-m/2*50, color="danger", bar=True),
            dbc.Progress(value=50, color='secondary', bar=True)
            ]
    progress = dbc.Progress(content,
                            style={'height': '50px'})
    table_content = [html.Tr([html.Td(progress, colSpan=5)]),
                     html.Tr([
                         html.Td("S'est beaucoup dégradée"),
                         html.Td("S'est un peu dégradée"),
                         html.Td("Est restée stable"),
                         html.Td("S'est un peu améliorée"),
                         html.Td("S'est beaucoup améliorée")
                         ], style={'text-align': "center"})]
    table = dbc.Table(table_content)
    return table


def categorie_info(data, categorie):
    """
    Revoie des informations (badge et histogramme) pour une catégorie.

    Parameters
    ----------
    data : pandas.DataFrame
        Données à partir desquelles sont déterminées les valeurs de retour.
    categorie : str
        Nom de la catégorie.

    Returns
    -------
    badge : dash_bootstrap-components.Badge
        Badge dont le contenu les la note et dont la couleur est adaptée.
    histogramme : plotly.graph_objects.Figure
        Histograme de la répartition des notes de la catégorie.

    """
    note = round(data[categorie.upper()].mean(), 2)
    b = progress(note)
    histogramme = px.histogram(data[categorie],
                               range_x=[0.5, 6.5],
                               title='Répartition des notes des répondants \
                               pour la catégorie')
    return b, histogramme


def question_info(data, question):
    """
    Renvoie les informations concernant une question du baromètre.

    Parameters
    ----------
    data : pandas.DataFrame
        Données à partir desquelles sont calculées les informations.
    question : str
        intitulé de la question à analyser.

    Returns
    -------
    badge : dash_bootstrap_components.Badge
        Badge contenant la note moyenne à la question et dont la couleur est
        ajustée en fonction.
    histogram : plotly.graph_objects.Figure
        histogramme de la répartition des notes sur la question.

    """
    my_question = questions[question]
    q = my_question['question']
    labels = [k + '-' + v if v else k
              for k, v in my_question['answer'].items()]
    note = round(data[question].astype(float).mean(), 2)
    b = progress(note)
    h = data[question].value_counts()
    bins = [int(i) for i in my_question['answer'].keys()]
    for i in bins:
        if i not in h:
            h[i] = 0
    count = [h[i] for i in bins]
    histogram = px.bar(x=labels, y=count, title=q, labels={'x': '', 'y': ''})
    return b, histogram


def question_histogramme(data, question):
    """
    Renvoi l'histogramme de répartition des notes à la question.

    Parameters
    ----------
    data : pandas.DataFrame
        Données à partir desquelles est établi l'histogramme.
    question : str
        Nom de la question dont on souhaite l'histogramme.

    Returns
    -------
    histogram : plotly.graph_objects.Figure
        Histogramme de répartition des notes sur la question.

    """
    my_question = questions[question]
    q = my_question['question']
    labels = [v if v else k for k, v in my_question['answer'].items()]
    h = data[question].value_counts()
    bins = [int(i) for i in my_question['answer'].keys()]
    for i in bins:
        if i not in h:
            h[i] = 0
    count = [h[i] for i in bins]
    histogram = px.bar(x=labels, y=count, title=q, labels={'x': '', 'y': ''})
    return histogram


def question_multiple_histogramme(data, question):
    """
    Renvoie l'histogramme des choix d'une question à choix multiples.

    Parameters
    ----------
    data : pandas.DataFrame
        Données à partir desquelles est établi l'histogramme.
    question : str
        Nom de la question dont on souhaite l'histogramme.

    Returns
    -------
    histogram : plotly.graph_objects.Figure
        Histogramme de répartition des réponses.
className="h-100 p-5 bg-light text-dark border rounded-3"
    """
    my_question = questions[question]
    q = my_question['question']
    labels = [v if v else k for k, v in my_question['answer'].items()]
    d = data[[question]].copy()
    d.loc[d[question].isna(), question] = ''
    d['l'] = d[question].apply(lambda v: [int(i) for i in v.split(',') if i])
    liste = []
    for ll in list(d['l']):
        liste.extend(ll)
    h = {k: liste.count(int(k)) for k in my_question['answer']}
    histogram = px.bar(x=labels,
                       y=h.values(),
                       title=q,
                       labels={'x': '', 'y': ''})
    return histogram


def commentaires(data):
    """
    Renvoie la liste des commentaires textuels.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame des données desquelles ont souhaite la liste des
        commentaires.

    Returns
    -------
    list
        liste de ListGroupItem dont le contenu sont les différents
        commentaires textuels.

    """
    d = data['q35'].copy()
    return [dbc.ListGroupItem(text) for text in d.dropna()]


def panel_content(categorie, qlist):
    """
    Renvoie un panneau pour la catégories.

    Parameters
    ----------
    categorie : str
        Nom de la catégorie.
    qlist : list
        liste des noms de question pour la catégories.

    Returns
    -------
    dahs_bootstrap_components.Container
        Container contenant les emplacements pour les informations de la
        catégorie et celles de différentes questions qui la composent.

    """
    content = [html.Div([
        html.H2(label[categorie], className="display-3"),
        html.Hr(className="my-2"),
        html.Span(id='note_'+categorie),
        html.Hr(className="my-2"),
        dcc.Graph(id='histogramme_'+categorie)
        ], className="h-100 p-5 text-white bg-primary rounded-3")]

    for i in qlist:
        content.append(html.Hr(className="my-2"))
        content.append(html.Div([
            html.H2([questions[i]['question']], className="display-3"),
            html.Hr(className="my-2"),
            html.Span(id='moyenne_'+i),
            html.Hr(className="my-2"),
            dcc.Graph(id='histogramme_'+i)
            ], className="h-100 p-5 bg-light text-dark border rounded-3"))

    return dbc.Container(content)
