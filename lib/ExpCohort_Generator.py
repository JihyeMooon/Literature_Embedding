#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 14:10:26 2022

@author: moon
"""

import pandas as pd 
import pathlib
import Literature_Data_Preprocessing as ldpl
feature_symbol = ['oca','bca','nit','fhha', 'sbld', 'pulrate']
feature_name = ['Other cancer','Breast cancer','Nitrates','Family history of heart attack','Systolic Blood Pressure (from Waveform Analysis), (mmHg)','Pulse Rate (from Waveform Analysis), (beats/minute)']
label_symbol=['mi','rca','ang','ptca','cbg']
label_name = ['Myocardial Infarction (MI)', 'Resuscitated Cardiac Arrest', 'Angina Pectoris', 'Percutaneous Transluminal', 'Coronary Angioplasty (PTCA)']


subject_number= 200
import random 
X=[]
y=[]
for n in range(subject_number):
    buffer=[]
    for i in range(len(feature_name)):
        buffer.append(random.random())
    X.append(buffer)
    y.append([random.randint(0, 1)])
Xt = pd.DataFrame(X, columns=feature_symbol)
y = pd.DataFrame(y) 


ldp=ldpl.preprocessing('', '', '', '') 
variables_indexing = {}
disease_variables_indexing = {}

for i in range(len(feature_name)):  
    buffer = ldp.sentence_preprocessor(feature_name[i]) 
    variables_indexing[feature_symbol[i]] = buffer 
    
for i in range(len(label_name)):  
    buffer = ldp.sentence_preprocessor(label_name[i]) 
    disease_variables_indexing[label_symbol[i]] = buffer 
    
example_path='../../data/Example/'
pathlib.Path(example_path).mkdir(parents=True, exist_ok=True)
Xt.to_csv(example_path+'Example_X.csv')
y.to_csv(example_path+'Example_y.csv')

pd.DataFrame(variables_indexing.values()).to_csv(example_path+'variables_preprocessed_names.csv')
pd.DataFrame(variables_indexing.keys()).to_csv(example_path+'variables_symbol.csv')

pd.DataFrame(disease_variables_indexing.values()).to_csv(example_path+'target_variables_preprocessed_names.csv')
pd.DataFrame(disease_variables_indexing.keys()).to_csv(example_path+'target_variables_symbol.csv')
