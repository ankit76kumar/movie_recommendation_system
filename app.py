import pickle
import streamlit as st
import requests
import difflib

# ============ Fetch poster with fallback ============
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except Exception as e:
        print("Poster fetch error:", e)
        return "https://via.placeholder.com/300x450?text=No+Image"

# ============ Recommend movies ============
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# ============ Load data ============
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ============ UI ============
st.header('🎬 Movie Recommender System')

# Dropdown select
movie_list = movies['title'].values
selected_movie = st.selectbox("📽️ Choose a movie from dropdown", movie_list)

# OR Search movie by name
search_input = st.text_input("🔎 Or search a movie by name")
searched_movie = None

if st.button("Search Movie Name"):
    all_titles = movies['title'].tolist()
    close_matches = difflib.get_close_matches(search_input, all_titles, n=1, cutoff=0.6)
    if close_matches:
        searched_movie = close_matches[0]
        st.success(f"✅ Found: {searched_movie}")
    else:
        st.warning("❌ No similar movie found. Try a different name.")

# Use searched movie (if any), otherwise use dropdown selection
final_movie = searched_movie if searched_movie else selected_movie

# Show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(final_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i])
            st.text(recommended_movie_names[i])
