# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:46:07 2022

@ Journal: Expert Systems With Applications
@ Title: A Literature Embedding Model for Cardiovascular Disease Prediction using Risk Factors, Symptoms, and Genotype Information
@ Accepted Date: Aug. 24, 2024
@ Author: Jihye Moon, Hugo F. Posada-Quintero, and *Ki. H. Chon
@ Contact Email: jihye.moon@uconn.edu 

""" 
import pathlib

import lib.CVD_risk_factor_search as ie
import sys
model = ie.run_intrisic_evaluation()

model_path = str(sys.argv[1]) #'../data/old_model'
output_path = str(sys.argv[2]) #'../results/demo_a'

queries = ['stroke', 'atrial fibrillation', 'ventricular fibrillation']
TOPNUM = 25
pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
sys.path.append('lib')
model.setting(path=model_path, gene_symb='../data/gene_name_info/query_symbol')

for query in queries:
    model.running(query, output_path, TOPNUM)







