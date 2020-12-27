import numpy as np
import pandas as pd
import warnings
from sklearn.feature_extraction.text import CountVectorizer
from annoy import AnnoyIndex
import pickle
from gensim.models import Word2Vec
import streamlit as st
import re
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)


class Model:
    def __init__(self):
        self.df = pd.read_csv('main_data.csv')
        self.w2v_model = Word2Vec.load('descr_w2v.model')
        self.genre_cv = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open('genres_vec.pkl', "rb")))
        self.annot_ann = AnnoyIndex(300 + len(self.genre_cv.vocabulary), 'angular')
        self.annot_ann.load('descr.ann')
        with open('genr_list.pkl', 'rb') as f:
            self.genre_list = pickle.load(f)

    def _clean(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\_', ' ', text)
        return text

    def find(self, name):
        name = set(self._clean(name).split())
        best = [0, 0]
        for i in range(len(self.df)):
            temp = set(self.df['title'][i].lower().split())
            if temp == name:
                return i
            elif len(name.intersection(temp)) > best[0]:
                best[0] = len(name.intersection(temp))
                best[1] = i
        return best[1]

    def to_vec(self, sent, genre):
        sent = sent.split()
        v = np.zeros((300,))
        for word in sent:
            if word in self.w2v_model:
                v += self.w2v_model.wv[word]
        v /= len(sent)
        gen = np.array(self.genre_cv.transform([genre]).todense())[0]
        v = np.hstack((v, gen))
        return v

    def give_books_name(self, name):
        ind = self.find(name)
        print(ind)
        av = self.to_vec(self.df['full_text'][ind], self.df['genres_x'][ind])
        arr_idx = self.annot_ann.get_nns_by_vector(av, 10)
        res = self.df.iloc[arr_idx, :].sort_values(by=['freq'], ascending=False).index
        return self.df[['author', 'title']].iloc[res]

    def give_books_descr(self, genres):
        key_words = ' '.join(genres)
        for i in range(len(genres)):
            genres[i] = self.genre_list[genres[i]]
        genres = ' '.join(genres)
        vec = self.to_vec(key_words, genres)
        arr_idx = self.annot_ann.get_nns_by_vector(vec, 50)
        res = self.df.iloc[arr_idx, :].sort_values(by=['freq'], ascending=False).index
        return self.df[['author', 'title']].iloc[res]
