from sklearn.feature_extraction.text import HashingVectorizer
import os
import pickle
import nltk

cur_dir = os.path.dirname(__file__)

vect = HashingVectorizer(decode_error='ignore',
                        stop_words='english',
                        n_features=2**21,
                        preprocessor=None,
                        tokenizer =nltk.word_tokenize,
                        )
