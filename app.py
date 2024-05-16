import streamlit as st
import pickle
import pandas as pd
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
import requests

import requests

def fetch_poster(movie_id):
    # Constructing the URL with the correct endpoint
    url = "https://api.themoviedb.org/3/movie/{}?api_key=90a899c27059548f5f19d61814d5e04c".format(movie_id)
    
    # Making the request
    response = requests.get(url, verify=False)
    
    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing JSON response
        data = response.json()
        
        # Checking if 'poster_path' is present in the response
        if 'poster_path' in data and data['poster_path'] is not None:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/original" + poster_path
            return full_path
        else:
            # Handle case where 'poster_path' is not present or is None
            return None
    else:
        # Handle case where request was unsuccessful
        print("Failed to fetch data from TMDb.")
        return None
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movie_posters = []
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters
option=st.selectbox('What would you like to watch?',movies['title'].values)
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(option)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(recommended_movie_names[i])
        if recommended_movie_posters[i] is not None:
            col.image(recommended_movie_posters[i])
        else:
            col.write("No poster available")
