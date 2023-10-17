import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api 
        recommended_movies_posters.append(fetch_poster(movie_id))
        
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender system')

Selected_movie_name = st.selectbox('Select The Movie That You Liked', movies['title'].values)


if st.button('Recommend'):
    names, posters = recommend(Selected_movie_name)
    
    # Create two rows with 3 columns each
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2 = st.columns(2)

    for i in range(5):
        if i < 3:
            with row1_col1 if i % 3 == 0 else row1_col2 if i % 2 == 0 else row1_col3:
                st.header(names[i])
                st.image(posters[i], use_column_width=True)
        else:
            with row2_col1 if i % 2 == 0 else row2_col2:
                st.header(names[i])
                st.image(posters[i], use_column_width=True)

