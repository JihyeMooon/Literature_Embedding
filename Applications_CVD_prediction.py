# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 21:59:06 2022

@author: Jihye Moon
"""
import sys
import os
import pathlib

import pandas as pd
import numpy as np
 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit as strata

import lib.ML_models as ml
sys.path.append('Literature_data_collection')   
import loading_literature_embedding as emb

def data_split(X_train_index, X_test_index, X, y):
    valid_data = int(len(X_test_index)/2) 
    test_data = int(len(X_test_index))-valid_data 
    
    test = X_test_index[0:test_data]; valid = X_test_index[test_data:test_data+valid_data] 
    
    X_train = X[X_train_index]; X_test = X[test]; X_valid = X[valid]
    
    y_train = y[X_train_index]
    y_test = y[test]
    y_valid = y[valid]
    
    X_train = np.reshape(X_train, (X_train.shape[0], -1)); X_test = np.reshape(X_test, (X_test.shape[0], -1))
    X_valid = np.reshape(X_valid, (X_valid.shape[0], -1)) 
    y_train = np.squeeze(y_train); y_test = np.squeeze(y_test); y_valid = np.squeeze(y_valid) 
                 
    scaler = StandardScaler()  
    scaler.fit(X_train)
    X_train = scaler.transform(X_train); X_test = scaler.transform(X_test); X_valid = scaler.transform(X_valid) 
    return X_train, X_test, X_valid, y_train, y_test, y_valid

def loading_variable_embedding():
    var_symbol = list(pd.read_csv('../data/variables_symbol.csv').drop(columns='Unnamed: 0')['0'])
    var_name = list(pd.read_csv('../data/variables_preprocessed_names.csv').drop(columns='Unnamed: 0')['0'])
    tar_symbol = list(pd.read_csv('../data/target_variables_symbol.csv').drop(columns='Unnamed: 0')['0'])
    tar_name = list(pd.read_csv('../data/target_variables_preprocessed_names.csv').drop(columns='Unnamed: 0')['0'])
    
    variables_indexing={}; disease_variables_indexing={}
        
    for i in range(len(var_name)):
        variables_indexing[var_symbol[i]] = var_name[i]
        
    for i in range(len(tar_name)):
        disease_variables_indexing[tar_symbol[i]] = tar_name[i]
             
    additional_dictionary = {'uricosurics':'uricosuric'} 
    # If some variable names are very unique that can't find in embedding vocabulary, 
    # add the unique variable names here to avoid error for feature selection tasks
    
    embedding_list, index2variables, embedding, removal, removed_words = emb2simi.variable2embed(words_list, syn0norm, variables_indexing, additional_dictionary)
        
    if removal==[]:
        print(" === NO problem for your variables") 
        target_embedding_list, index2target, target_embedding, _, _ = emb2simi.variable2embed(words_list, syn0norm, disease_variables_indexing, additional_dictionary)
    
        return embedding_list, variables_indexing, disease_variables_indexing, additional_dictionary, \
            target_embedding_list, index2target, index2variables, target_embedding, embedding
    else:
        print(" === Check if there are errors for your variable names")
        return 0, 0, 0, 0, 0, 0, 0, 0, 0

def CVD_Prediction_with_FS_DR():
    feature_size = 128; i=0
    split_info = strata(n_splits=5, test_size=0.2, random_state=12)
    total_FS_Pre=[]; total_FS_prob=[]
    total_DR_pre=[]; total_DR_prob=[]
    embedding_list, variables_indexing, disease_variables_indexing, additional_dictionary, target_embedding_list, index2target, index2variables, target_embedding, embedding = loading_variable_embedding()
    for X_train_index, X_test_index in split_info.split(Xt.values, y): 
        result_dir = os.path.join(output_path +str(i)) 
        pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
        X_train, X_test, X_valid, y_train, y_test, y_valid = data_split(X_train_index, X_test_index, Xt.values, y)
        pr.save_label(y_test, 'CVD_label', result_dir) # y_test labels to evaludate CVD prediction performance for each fold
        print("=== run Our feature selector --- our FS selected features via feature name , our FS uses same feature set for 5-fold cross validation. ")
        embed_name = fs.Our_FS(emb2simi, str(i)+'rf_embedding_features', embedding_list, variables_indexing, disease_variables_indexing, additional_dictionary, embedding, target_embedding_list, index2target, index2variables, target_embedding, feature_size, result_dir)

        print("=== run Our dimensionality reductor ")
        A1, A2, A3 = dr.Our_DR(embedding, X_train, X_test, X_valid, feature_size)

        print("=== Running with MLs with Feature Selection (Our FS)")
        X2 = Xt[embed_name].values ### selecting only 128 variables based on our 128 features
        valid_data = int(len(X_test_index)/2); test_data = int(len(X_test_index))-valid_data 
        test = X_test_index[0:test_data]; valid = X_test_index[test_data:test_data+valid_data] # split test data 
        X_train2 = X2[X_train_index]; X_test2 = X2[test]; X_valid2 = X2[valid] 
        
        X_train2 = np.reshape(X_train2, (X_train2.shape[0], -1)) 
        X_test2 = np.reshape(X_test2, (X_test2.shape[0], -1))
        X_valid2 = np.reshape(X_valid2, (X_valid2.shape[0], -1))
        
        scaler = StandardScaler()  
        scaler.fit(X_train2)
        X_train2 = scaler.transform(X_train2); X_test2 = scaler.transform(X_test2); X_valid2 = scaler.transform(X_valid2) 
    
        Our_FS_total_prediction, Our_FS_total_prob = pr.run_save(X_train2, y_train, X_test2, y_test, X_valid2, y_valid, 'FS.embedding', 'SMOTE', feature_size, result_dir)
        total_FS_Pre.append(Our_FS_total_prediction); total_FS_prob.append(Our_FS_total_prob)
        print("=== Running MLs with Dimensionality Reduction (Our DR)")
        Our_DR_total_prediction, Our_DR_total_prob = pr.run_save(A1, y_train, A2, y_test, A3, y_valid, 'DR.embedding', 'SMOTE', feature_size, result_dir)
        total_DR_pre.append(Our_FS_total_prediction); total_DR_prob.append(Our_FS_total_prob)
        i+=1
    print('all results are saved in ', output_path)
    return total_FS_Pre, total_FS_prob, total_DR_pre, total_DR_prob

output_path = str(sys.argv[1]) #'../results/CVD_prediction_results' 
model_path = str(sys.argv[2]) #'../data/old_model'
X_path = str(sys.argv[3]) #'../data/MESA_X.csv'
y_path = str(sys.argv[4]) #'../data/MESA_y.csv'

fs = ml.feature_selectors()
dr = ml.dimension_reducers()
pr = ml.predictors()

gene_name = '../data/gene_name_info/query_full_name'; gene_symb='../data/gene_name_info/query_symbol' 
emb2simi=emb.embedding_vector()  

words_list, index2word, syn0norm, _ = emb2simi.setting(model_path, gene_symb) 

Xt = pd.read_csv(X_path).drop(columns='Unnamed: 0')
y = pd.read_csv(y_path).drop(columns='Unnamed: 0').values

total_FS_Pre, total_FS_prob, total_DR_pre, total_DR_prob = CVD_Prediction_with_FS_DR()
