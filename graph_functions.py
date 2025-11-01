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
with open('./questions.json','r') as fd:
    questions = json.load(fd)

color = {'A+':'rgb(43,121,16)',
         'A':'rgb(75,152,51)',
         'B':'rgb(121,181,45)',
         'C':'rgb(200,210,39)',
         'D':'rgb(254,239,48)',
         'E':'rgb(252,203,44)',
         'F':'rgb(243,153,57)',
         'G':'rgb(228,55,35)'}


def categorie_info(data,categorie) : 
    note = round(data[categorie].mean(),2)
    class_name = 'A+' if note>4.6 else 'A' if note > 4.3 else 'B' if note > 3.9 else 'C' if note > 3.5 else 'D' if note > 3.1 else 'E' if note > 2.7 else 'F' if note > 2.3 else 'G'
    badge = dbc.Badge([class_name+' : '+str(note)],color=color[class_name])
    histogramme = px.histogram(data[categorie],range_x=[0.5,6.5],title='Répartition des notes des répondants pour la catégorie')
    return badge,histogramme
    
def question_info(data,question) : 
    my_question = questions[question]
    q = my_question['question']
    labels = [k+ '-' +v if v else k for k,v in my_question['answer'].items()]
    moyenne = round(data[question].astype(float).mean(),2)
    
    class_name = 'A+' if moyenne>4.6 else 'A' if moyenne > 4.3 else 'B' if moyenne > 3.9 else 'C' if moyenne > 3.5 else 'D' if moyenne > 3.1 else 'E' if moyenne > 2.7 else 'F' if moyenne > 2.3 else 'G'
           
    badge = dbc.Badge([class_name+' : '+str(moyenne)],color=color[class_name])
    
    h = data[question].value_counts()
    bins = [int(i) for i in my_question['answer'].keys()]
    
    for i in bins:
        if not i in h:
            h[i]=0
    
    count = [h[i] for i in bins]
    histogram = px.bar(x=labels, y = count, title=q,labels={'x':'','y':''})
     
    return badge,histogram

def question_histogramme(data,question):
    my_question = questions[question]
    q = my_question['question']
    labels = [v if v else k for k,v in my_question['answer'].items()]
    h = data[question].value_counts()
    bins = [int(i) for i in my_question['answer'].keys()]
    
    for i in bins:
        if not i in h:
            h[i]=0
    
    count = [h[i] for i in bins]
    histogram = px.bar(x=labels, y = count, title=q,labels={'x':'','y':''})
    return histogram

def question_multiple_histogramme(data,question):
    my_question = questions[question]
    q = my_question['question']
    labels = [v if v else k for k,v in my_question['answer'].items()]
    d = data[[question]].copy()
    d.loc[d[question].isna(),question]=''
    d['l'] = d[question].apply(lambda v : [int(i) for i in v.split(',') if i])
    l = []
    for ll in list(d['l']):
        l.extend(ll)
    h = {k:l.count(int(k)) for k in my_question['answer']}
    histogram = px.bar(x=labels, y = h.values(), title=q,labels={'x':'','y':''})
    return histogram

def commentaires(data):
    
    d = data['q35'].copy()
    
    return [dbc.ListGroupItem(text) for text in d.dropna()]

def panel_content(categorie,qlist):
    content = [html.H3(['Note moyenne pour la catégorie : ',html.Span('',id='note_'+categorie)]),
               dcc.Graph(id='histogramme_'+categorie)
               ]
    
    for i in qlist:
        content.extend([
            html.H2([questions[i]['question']]),
            html.H3(['Note moyenne pour la question : ',html.Span('',id='moyenne_'+i)]),
            dcc.Graph(id='histogramme_'+i)
            ])
    return dbc.Container(content)
