# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 20:18:05 2022

@author: Jihye Moon
"""
import os 
import numpy as np
import math
import pathlib
from Moon_gene2vec import Gene2vec
import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector

class building_embedding_model():
    def __int__(self):
        return None
    
    def setting(self,preprocessed_path, vocab_dir, logs_dir, gene2doc_dir, baseline_doc_dir):
        
        self.baseline_doc_dir=baseline_doc_dir
        self.logs_dir=logs_dir
        self.gene2doc_dir=gene2doc_dir
        self.vocab_dir=vocab_dir
        
        self.gene2document =  os.path.join(preprocessed_path, 'gene2document.data.doc.txt')
        self.baseline_doc =  os.path.join(preprocessed_path, 'baseline_doc.data.doc.txt')

        return None
    
    def dumpArrayFile(self,denseList, path, name):
        np.asarray(denseList).dump(os.path.join(path, name+'.dat'))

    def creating_vocab(self, min_count = 5, min_size = 2): 
        g2v = Gene2vec()
        gene2doc, gene1 = g2v.data_loading(self.gene2document)
        baseline_doc, gene2 = g2v.data_loading(self.baseline_doc)
        
        vocaburary = g2v.vocab_output()
        
        removed_voc = g2v.selecting_vocab(vocaburary, min_count, min_size=min_size)  
        gene_dict, gene_reverse_dict = g2v.gene_dic(gene1, removed_voc)
         
        g2v.vocab_save('excluded_sum'+str(min_count)+'two2doc', gene_dict, self.vocab_dir)
           
        self.gene2doc=gene2doc
        self.gene1=gene1
        self.baseline_doc=baseline_doc
        self.gene_dict=gene_dict 
        self.gene_reverse_dict=gene_reverse_dict
        self.g2v=g2v
        self.vocabulary_size = len(self.gene_reverse_dict)
        
    def creating_training_data_for_gene2doc(self, window_size):
        g2v=self.g2v
        window_size=window_size
        gene1=self.gene1 
        gene_dict=self.gene_dict
        buf_batch=[]; buf_labels=[] 
        
        countData=0; indexing=0
        
        for i in range(len(self.gene2doc)):
            save_batch, save_labels = g2v.gene2doc_batch_fucntion(self.gene2doc[i], gene1[i], i, window_size) 
            save_batch, save_labels = g2v.gene_insert(save_batch,save_labels, gene_dict[gene1[i]]) 
            save_batch3, save_labels3 = g2v.gene_additing(self.gene2doc[i], gene_dict[gene1[i]], i, window_size)
            save_batch=np.concatenate((save_batch,save_batch3))
            save_labels=np.concatenate((save_labels,save_labels3)) 
                
            buf_batch.extend(save_batch)
            buf_labels.extend(save_labels) 
            if countData==1000: 
                self.dumpArrayFile(buf_batch, self.gene2doc_dir, 'batch.'+str(indexing))
                self.dumpArrayFile(buf_labels, self.gene2doc_dir, 'label.'+str(indexing))
                countData=0
                buf_batch=[]; buf_labels=[]
                indexing+=1
            countData+=1
        self.dumpArrayFile(buf_batch, self.gene2doc_dir, 'batch.'+str(indexing))
        self.dumpArrayFile(buf_labels, self.gene2doc_dir, 'label.'+str(indexing)) 
        del self.gene2doc

    def checking_gene2doc_generation(self, window_size):
        g2v=self.g2v
        window_size=window_size
        gene1=self.gene1 
        gene_reverse_dict=self.gene_reverse_dict
        
        for i in range(1):
            print("== Examples: ", gene1[i])
            save_batch, save_labels = g2v.gene2doc_batch_fucntion(self.gene2doc[i], gene1[i], i, window_size) 
            save_batch, save_labels = g2v.gene_insert(save_batch,save_labels, self.gene_dict[gene1[i]]) 
            save_batch3, save_labels3 = g2v.gene_additing(self.gene2doc[i], self.gene_dict[gene1[i]], i, window_size)
            save_batch=np.concatenate((save_batch,save_batch3)) 
            save_labels=np.concatenate((save_labels,save_labels3))  
        print("============================== Fig. 3(a) in the published paper ")
        for k in range(30): 
            print(gene_reverse_dict[save_batch[k]], '->' , gene_reverse_dict[save_labels[k]])
        print("============================== Fig. 3(b) in the published paper")
        for n in range(30): 
            k=len(save_batch)-1-n
            print(gene_reverse_dict[save_batch[k]], '->' , gene_reverse_dict[save_labels[k]]) 
        
    def creating_training_data_for_word2doc(self, window_size):
        g2v=self.g2v
        buf_batch=[]
        buf_labels=[] 
        window_size=window_size
        countData=0; indexing=0
        for i in range(len(self.baseline_doc)):
            save_batch, save_labels = g2v.gene2doc_batch_fucntion(self.baseline_doc[i], 0, i, window_size)  
            buf_batch.extend(save_batch)
            buf_labels.extend(save_labels) 
            if countData==50000:
                print(i, len(self.baseline_doc))
                self.dumpArrayFile(buf_batch, self.baseline_doc_dir, 'batch.'+str(indexing))
                self.dumpArrayFile(buf_labels, self.baseline_doc_dir, 'label.'+str(indexing))
                countData=0
                buf_batch=[]; buf_labels=[]
                indexing+=1
            countData+=1
        self.dumpArrayFile(buf_batch, self.baseline_doc_dir, 'batch.'+str(indexing))
        self.dumpArrayFile(buf_labels, self.baseline_doc_dir, 'label.'+str(indexing)) 
    
    def model_setting(self, dimension, num_sampled):
        self.vocabulary_size = len(self.gene_reverse_dict)
        self.dimension = dimension
        self.num_sampled = num_sampled
            
    def sorting_data_loading(self, data): 
        batch=[]
        label=[]
        full_size=int(len(data)/2)
        for i in range(full_size):
            batch.append('batch.'+str(i)+'.dat')
            label.append('label.'+str(i)+'.dat')
        return batch, label
    
    def logs(self, name, word):
        f = open(name+'_logs.txt','a') 
        f.write('{}\n'.format(word))
        f.close()
        
    def starting_sorting(self, model_path):
        import argparse
        print('starting making data')
        logs_dir=self.logs_dir
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--log_dir',
            type=str,
            default=model_path,
            help='The log directory for TensorBoard summaries.')

        FLAGS, unparsed = parser.parse_known_args()
        self.FLAGS = FLAGS
        if not os.path.exists(FLAGS.log_dir):
            os.makedirs(FLAGS.log_dir)
        dir_names = os.listdir(logs_dir)
        batch_list_dir=[]; target_list_dir=[]
        for i in range(len(dir_names)):
            if '.txt' not in dir_names[i]: 
                print(i, dir_names[i])
                data_dir = os.path.join(logs_dir, dir_names[i]) 
                result = os.listdir(data_dir)
                
                batch_rd, label_rd = self.sorting_data_loading(result)
                for j in range(len(batch_rd)):
                    if 'batch' in batch_rd[j]:
                        batch_list_dir.append(os.path.join(data_dir, batch_rd[j]))
                        self.logs(os.path.join(FLAGS.log_dir, 'batch_list'), os.path.join(data_dir, batch_rd[j]))
                for j in range(len(label_rd)):
                    if 'label' in label_rd[j]:
                        target_list_dir.append(os.path.join(data_dir, label_rd[j]))
                        self.logs(os.path.join(FLAGS.log_dir, 'target_list'), os.path.join(data_dir, label_rd[j]))
            self.target_list_dir=target_list_dir
            self.batch_list_dir=batch_list_dir
        
    def batch(self, X, y, batch_size, name='batch'): 
        n_size=len(X)
        rd_idx = np.random.permutation(n_size) 
        n_batches = n_size // batch_size
        for idx in np.array_split(rd_idx, n_batches):
            X_batch, y_batch = X[idx], y[idx]
            yield X_batch, y_batch
             
    def model_training(self, epoch=10, batch_size=256): 
        all_size = len(self.batch_list_dir)
        vocabulary_size=self.vocabulary_size
        dimension=self.dimension
        num_sampled=self.num_sampled
        
        valid_size = 16   
        valid_window = 100  
        valid_examples = np.random.choice(valid_window, valid_size, replace=False)
        num_steps = epoch
        graph = tf.Graph()
        
        with graph.as_default(): 
          # Input data.
          with tf.name_scope('inputs'):
            train_inputs = tf.placeholder(tf.int32, shape=[None])
            train_labels = tf.placeholder(tf.int32, shape=[None, 1])
            valid_dataset = tf.constant(valid_examples, dtype=tf.int32)
        
          with tf.device('/cpu:0'):
            nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size, dimension],
                                            stddev=1.0 / math.sqrt(dimension)), name='nce_w')
            nce_biases = tf.Variable(tf.zeros([vocabulary_size]), name='nce_b')
            embeddings = tf.Variable(tf.random_uniform([vocabulary_size, dimension], -1.0, 1.0), name='embed1') 
            embed = tf.nn.embedding_lookup(embeddings, train_inputs, name='lookup')
        
          with tf.name_scope('loss'):
            loss = tf.reduce_mean(
                tf.nn.nce_loss(
                    weights=nce_weights, 
                    biases=nce_biases,
                    labels=train_labels,
                    inputs=embed,
                    num_sampled=num_sampled,
                    num_classes=vocabulary_size))
            
          tf.summary.scalar('loss', loss)
          with tf.name_scope('optimizer'):
            optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss)
        
          norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
          normalized_embeddings = embeddings / norm
          valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
          similarity = tf.matmul(
              valid_embeddings, normalized_embeddings, transpose_b=True)
        
          merged = tf.summary.merge_all()
          init = tf.global_variables_initializer()
          saver = tf.train.Saver()
        
        savedloss=[]
        with tf.Session(graph=graph) as session:
            writer = tf.summary.FileWriter(self.FLAGS.log_dir, session.graph)
            init.run()  
                    
            print('Initialized') 
            average_loss = 0;
            counting=0; total_counting=0;
            with open(self.FLAGS.log_dir + '/metadata.tsv', 'w', encoding='UTF-8') as f:
                for i in range(vocabulary_size):
                    f.write(self.gene_reverse_dict[i] + '\n')
            for step in range(num_steps): 
                rd_idx = np.arange(all_size)
                np.random.shuffle(rd_idx)
                for rn in rd_idx:  
                    batch_dir = self.batch_list_dir[rn]
                    label_dir = self.target_list_dir[rn] 
                    target=np.load(batch_dir, allow_pickle=True)
                    label=np.load(label_dir, allow_pickle=True)
                    loading_target=target
                    loading_label=label
                    full_size=len(loading_label) 
                    if step % full_size==0:
                        full_size=len(loading_label)
                        rd = np.arange(full_size)
                        np.random.shuffle(rd) 
                        loading_label=loading_label[rd]
                        loading_target=loading_target[rd]
                        loading_target=loading_target[rd] 
                    for X_batch, y_batch in self.batch(X= target, y=label, batch_size = batch_size): 
                        y_batch=y_batch.reshape(-1,1)
                        feed_dict = {train_inputs: X_batch, train_labels: y_batch} 
                        run_metadata = tf.RunMetadata() 
                        _, summary, loss_val = session.run(
                            [optimizer, merged, loss],
                            feed_dict=feed_dict,
                            run_metadata=run_metadata)
                        average_loss += loss_val
                        counting+=1; total_counting+=1;
                        writer.add_summary(summary, step)
                writer.add_run_metadata(run_metadata, 'step%d' % step)
                average_loss /= counting
                print('Average loss at step ', step, '/', num_steps, ': ', average_loss) 
                self.logs(os.path.join(self.FLAGS.log_dir, '128d'), str(step)+' '+str(average_loss))
                savedloss.append(average_loss)
                average_loss = 0
                counting=0 
                saver.save(session, os.path.join(self.FLAGS.log_dir, 'mid_model.ckpt')) 
                self.dumpArrayFile(self.gene_reverse_dict, self.FLAGS.log_dir, 'name')  
                sim = similarity.eval()
                for i in range(valid_size):
                    valid_word = self.gene_reverse_dict[valid_examples[i]]
                    top_k = 8  # number of nearest neighbors
                    nearest = (-sim[i, :]).argsort()[1:top_k + 1]
                    log_str = 'Nearest to %s:' % valid_word
                    for k in range(top_k):
                      close_word = self.gene_reverse_dict[nearest[k]]
                      log_str = '%s %s,' % (log_str, close_word)
                    print(log_str)
            config = projector.ProjectorConfig()
            embedding_conf = config.embeddings.add()
            embedding_conf.tensor_name = embeddings.name
            embedding_conf.metadata_path = os.path.join(self.FLAGS.log_dir, 'metadata.tsv') 
            
            saver.save(session, os.path.join(self.FLAGS.log_dir, 'model.ckpt'))
          
        writer.close() 