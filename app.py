import streamlit as st
import pandas as pd
from Predictor import Model

st.title('СЕРВИС: КНИЖНЫЙ ЧЕРВЬ')
st.header('Подберём похожие книги по названию')
model = Model()
book_title = st.text_input('Введи названия любимой книги')
result1 = model.give_books_name(book_title)
result1.columns = ['Автор', 'Название']
result1.reset_index(drop=True, inplace=True)
st.write(result1)

st.header('Подберём книги по жанру')
genres = st.multiselect('выбери жанры', list(model.genre_list.keys()))

result2 = model.give_books_descr(genres)
result2.columns = ['Автор', 'Название']
result2.reset_index(drop=True, inplace=True)
st.write(result2)