import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
import re
import io
import numpy as np

data = pd.read_csv('data.csv')

in_tokenizer = Tokenizer(filters='', split=" ")
in_tokenizer.fit_on_texts(data["error"])
out_tokenizer = Tokenizer(filters='', split=" ")
out_tokenizer.fit_on_texts(data["correct"])
def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = np.asarray(tokens[1:])#map(float, tokens[1:])
    return data

embedding_index = load_vectors('wiki-news-300d-1M.vec')

def word2vec(word_index):
	embedding_dim = 300
	num_tokens = len(word_index) + 2
	embedding_matrix = np.zeros((num_tokens, embedding_dim))
	for word, i in word_index.items():
	    embedding_vector = embedding_index.get(word)
	    if type(embedding_vector) == np.ndarray and embedding_vector.shape[0] == 300:  
	        embedding_matrix[i] = embedding_vector
	return embedding_matrix

np.save('in_embedding.npy', word2vec(in_tokenizer.word_index))
np.save('out_embedding.npy', word2vec(out_tokenizer.word_index))
