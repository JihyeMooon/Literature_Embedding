# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 00:16:25 2020

"""

import os
import pathlib 
import sys

sys.path.append('lib')  
from Literature_Data_Collection import literature_data_collection

if len(sys.argv)>3:
    word_query = str(sys.argv[1])
    word_end_point = int(sys.argv[2]) # the endpoint of a word-based data collection. for demo-b 100000
    gene_end_point = int(sys.argv[3]) # the endpoint of gene name-based data collection for demo-b 50
    paths = str(sys.argv[4]) + '/'
elif len(sys.argv)==3:
    word_query = str(sys.argv[1])
    paths = str(sys.argv[2]) + '/'
     
data_dir = os.path.abspath(os.getcwd())
output_dir = os.path.join(data_dir, paths + 'baseline_doc')
document_output_dir = os.path.join(data_dir, paths + 'gene2document') 
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(document_output_dir).mkdir(parents=True, exist_ok=True)
email = "request00@gmail.com" # default

ld = literature_data_collection(email, output_dir, document_output_dir) # setting up

########### word query based literature data collection ################# 
gap=50000
batch = 10000
w2d_starting_point = 0  

search_results, _word_end_point = ld.word_based_query_fit(year = None, user_term=word_query)
print('The number of avaliable abstracts :', _word_end_point, 'for ', word_query) 

if int(sys.argv[2])==0:
    word_end_point = _word_end_point
ld.collecting_doc_using_word_based_query(year = None, user_term=word_query, gap = gap, starting = gap*w2d_starting_point, ixs = w2d_starting_point, test_end_point=word_end_point)

########### gene name-query based literature data collection ################# 
query_full=ld.text_open('../data/gene_name_info/query_full_name.txt')
query_symbol=ld.text_open('../data/gene_name_info/query_symbol.txt') # gene name list

query_size = len(query_full)
ld.gene_based_query_fit(query_size, query_full, query_symbol) # setting up

g2d_starting_point = 0 
batch_size = 10
#############################
#####################
gene_end_point = round(query_size/batch_size)

if len(sys.argv)>2:
    gene_end_point = int(sys.argv[3]) # the endpoint of gene name-based data collection 
if int(sys.argv[3])==0:
    gene_end_point = round(query_size/batch_size)
ld.collecting_doc_using_gene_based_query(year = None, batch_size = batch_size, starting = g2d_starting_point, query_len=len(query_full), end_point = gene_end_point)
