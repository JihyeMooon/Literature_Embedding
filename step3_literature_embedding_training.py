"""
Created on Sun Jun 21 00:16:25 2020

@author: Jihye Moon

"""
 
import pathlib
import sys
sys.path.append('lib')  
import Building_Literature_Embedding_Model as edg

window_size = 2
min_count = 5
min_size = 2
dimension = 128
num_sampled = 16
batch_size = 564 #256
epoch = 10

root_path = sys.argv[1] #
epoch = int(sys.argv[2])
output = sys.argv[3]

vocab_dir = output + '/vocab/'
preprocessed_path = root_path + '/preprocessed'
model_path = output 
logs_dir = vocab_dir+'/logs'
gene2doc_dir = logs_dir+'/gene2doc'
baseline_doc_dir = logs_dir+'/baseline_doc'

pathlib.Path(logs_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(gene2doc_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(baseline_doc_dir).mkdir(parents=True, exist_ok=True)
pathlib.Path(model_path).mkdir(parents=True, exist_ok=True)

print("==== Generating Training Data for Literature Embedding Model")
eg=edg.building_embedding_model()
eg.setting(preprocessed_path, vocab_dir, logs_dir, gene2doc_dir, baseline_doc_dir)

print("==== Creating Vocabulary ===")
eg.creating_vocab()

print("=== Checking If Data Generation Is Correct ===")
eg.checking_gene2doc_generation(window_size)
print("=== Creating Training Data For Fig. 3(a) and (b) in our paper ===")
eg.creating_training_data_for_gene2doc(window_size)

print("=== Creating Training Data For Fig. 2 in our paper ===")
eg.creating_training_data_for_word2doc(window_size)

print("=== Starting Model Training For Figs.2-3 ===")
eg.model_setting(dimension=dimension, num_sampled=num_sampled)
eg.starting_sorting(model_path)
eg.model_training(epoch=epoch, batch_size=batch_size)


