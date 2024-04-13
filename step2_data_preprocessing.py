# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 00:16:25 2020

@author: Jihye Moon

"""

import os
import pathlib
import sys

sys.path.append('lib')  
import Literature_Data_Preprocessing as ldp

base = sys.argv[1]
output = sys.argv[2]
batch_dir = base # os.path.join(base, 'literature_data')
comb_dir = os.path.join(base, 'arranged')
preprocessed_dir = os.path.join(output, 'preprocessed')
pathlib.Path(comb_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(preprocessed_dir).mkdir(parents=True, exist_ok=True)
 
lp=ldp.preprocessing(base, batch_dir, comb_dir, preprocessed_dir) 

### Extracting only abstracts and combining all collected files into one file (Gene name based documents)
file_names, data_list=lp.batch_data_matching(batch_dir, ['gene2document'])
arr_list = lp.combining_files(file_names, data_list, ['FullText'], 3)

for i in range(len(file_names)):
    lp.Indexing(os.path.join(comb_dir, file_names[i]), arr_list[file_names[i]])
    
gene2doc = lp.gene2doc_mapping(arr_list[file_names[0]])
 

### Extracting only abstracts and combining all collected files into one file (Word name based documents)
file_names_doc, data_list_doc = lp.batch_data_matching(batch_dir, ['baseline_doc'])
arr_list2 = lp.combining_query2doc(file_names_doc, data_list_doc, ['pubmed'], 4) 


### Literature Data Preprocessing
total_FullText = ''; total_meta = ''
total_size=len(arr_list2[file_names_doc[0]])
full_handle = open(os.path.join(comb_dir, file_names_doc[0]+'.FullText.txt'), "w")
meta_handle = open(os.path.join(comb_dir, file_names_doc[0]+'.meta.txt'), "w")

total_FullText=[]
for i in range(total_size):
    FullText, Meta = lp.Medine_mapping(arr_list2[file_names_doc[0]][i]) 
    #print(i, '/', total_size, round(i/total_size,2)*100)
    total_FullText.append(FullText)
    full_handle.write(FullText)
    meta_handle.write(Meta)
full_handle.close()
meta_handle.close()

doc_gene=list(gene2doc.keys())

print('----- preprocessing --- for gene name based documents')
lp.making_doc_data(doc_gene, file_names[0], gene2doc) 

print('----- preprocessing --- for word name based documents')
lp.making_doc_data(None, file_names_doc[0], total_FullText)
