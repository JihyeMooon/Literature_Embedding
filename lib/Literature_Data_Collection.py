# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 17:28:57 2022

@author: Jihye Moon
"""

import os
import time
from Loading_PudMed import ids_pudmed as pudmed

class literature_data_collection():
    def __init__(self, email, output_dir, document_output_dir):
        self.output_dir=output_dir
        self.document_output_dir=document_output_dir
        self.email = email 
    
    def text_open(self, path):
        with open(path, 'r') as f:
            data=f.read().strip().split('\n')
        return data
    
    def data_split(self, key):
        return key.split('#')
    
    def word_based_query_fit(self, year = None, user_term="heart"):
        email = self.email
        pud = pudmed() 
        search_results, end_point = pud.search_list(user_term, year, email) 
        return search_results, end_point 
    
    def collecting_doc_using_word_based_query(self, year = None, user_term="heart", gap = 50000, starting = 0, ixs = 0, test_end_point=0):
        email = self.email
        pud = pudmed() 
        search_results, end_point = pud.search_list(user_term, year, email) 
        batch = 10000
        gap=gap
        
        if test_end_point != 0:
            end_point = test_end_point # Test 
            print('Checking data collection performance --- collecting until ',end_point,' documents')
            
        counting=round(end_point/gap) 
         
        starting = starting 
        ending = starting + gap 

        for ix in range(ixs, counting):
            #if ix == counting-1:
            #    starting = ending
            #    ending = end_point
            print(ix, '/', counting -1, ' | from ', starting, ' to ', ending) 
            pud.search_full(ix, self.output_dir, search_results, starting, ending, batch)

            starting = ending
            ending = starting+gap 
    
            if ix == counting-1:
                ending = end_point
                
    def collecting_doc_using_word_based_query2(self, batch = 10000, gap = 50000, starting = 0, ixs = 0, search_results={}, end_point=0):

        pud = pudmed() 
        
        gap=gap 
            
        counting=round(end_point/gap) 
         
        starting = starting 
        ending = starting + gap 

        for ix in range(ixs, counting):
            print(ix, '/', counting -1, ' | from ', starting, ' to ', ending) 
            pud.search_full(ix, self.output_dir, search_results, starting, ending, batch)

            starting = ending
            ending = starting+gap 
            if ix == counting-1:
                ending = end_point
    
    def gene_based_query_fit(self, query_len, query_full, query_symbol):
        self.query_len=query_len
        self.query_symbol=query_symbol
        self.query_full=query_full
    
    def collecting_doc_using_gene_based_query(self, year = None, batch_size = 10, starting = 0, query_len = 26335, end_point = 2634):
        document_output_dir=self.document_output_dir
        counting=starting*batch_size
        query_len=self.query_len
        query_symbol=self.query_symbol
        query_full=self.query_full
        email = self.email
        pud = pudmed() 
        
        for i in range(starting, end_point+1): 
            handle2 = open(os.path.join(document_output_dir, "FullText_symbol."+str(i)+".txt"), "w")
            handle_excluding2 = open(os.path.join(document_output_dir, "excluded_symbol."+str(i)+".txt"), "w")
            handle_meta2 = open(os.path.join(document_output_dir, "meta_symbol."+str(i)+".txt"), "w") 
            print('Collecting Gene2doc ',i , '/', end_point)
            for j in range(batch_size):
                if counting>=query_len-1:
                    break; 
                time.sleep(5)
                LR2, FullText2, meta2 = pud.search_gene2doc(query_symbol[counting], email)
         
                if LR2!=[]:
                    indexing2 = str(counting)+'\t'+query_symbol[counting]+'\t'+query_full[counting]+FullText2
                    handle2.write(indexing2)
                    handle_meta2.write(str(counting)+'\t'+query_symbol[counting]+'\t'+query_full[counting]+meta2)
                else: 
                    handle_excluding2.write(query_symbol[counting]+'\t'+query_full[counting]+'\n')
                counting += 1 
            handle_excluding2.close()
            handle_meta2.close()
            handle2.close() 
 