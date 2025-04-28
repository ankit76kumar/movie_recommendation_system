#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')


# In[3]:


credits


# In[4]:


movies


# In[5]:


movies.columns


# In[6]:


credits.columns


# In[7]:



movies.head(2)


# In[8]:



credits.head()


# In[9]:


movies.tail(3)  


# In[10]:


credits.tail(5)


# In[11]:


movies.info()


# In[12]:


credits.info()


# In[13]:


credits.describe() 


# In[14]:


movies.describe() 


# In[15]:


credits.corr()


# In[16]:


movies.corr()


# In[17]:


movies.index  


# In[18]:


credits.index  


# In[19]:


movies.shape


# In[20]:


credits.shape


# In[21]:


movies.dtypes 


# In[22]:


# List all columns with dtype 'object'
movies.select_dtypes(include='object').columns


# In[23]:


# List all columns with dtype int64
movies.select_dtypes(include='int64').columns


# In[24]:


credits.dtypes 


# In[25]:


credits.isnull().sum()


# In[26]:


movies.isnull().sum()


# In[27]:


movies = movies.merge(credits,on='title')


# In[28]:


movies


# In[29]:


movies.shape


# In[30]:


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[31]:


movies


# In[32]:


import ast


# In[33]:


def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 


# In[34]:


movies.dropna(inplace=True)


# In[35]:


movies['genres'] = movies['genres'].apply(convert)
movies.head()


# In[36]:


movies['keywords'] = movies['keywords'].apply(convert)
movies.head()


# In[37]:


import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[38]:


def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L 


# In[39]:


movies['cast'] = movies['cast'].apply(convert)
movies.head()


# In[40]:


movies['cast'] = movies['cast'].apply(lambda x:x[0:3])


# In[41]:


def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L 


# In[42]:


movies['crew'] = movies['crew'].apply(fetch_director)


# In[43]:


movies


# In[44]:


movies.sample(5)


# In[45]:


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


# In[46]:


movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)


# In[47]:


movies


# In[48]:


movies['overview'] = movies['overview'].apply(lambda x:x.split())


# In[49]:


movies


# In[50]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[51]:


movies


# In[52]:


movies["tags"]


# In[53]:


new = movies.drop(columns=['overview','genres','keywords','cast','crew'])
#new.head()


# In[54]:


new


# In[55]:


new['tags'] = new['tags'].apply(lambda x: " ".join(x))
new.head()


# In[56]:


new


# In[57]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


# In[58]:


vector = cv.fit_transform(new['tags']).toarray()


# In[59]:


vector


# In[60]:


vector.shape


# In[61]:


from sklearn.metrics.pairwise import cosine_similarity


# In[62]:


similarity = cosine_similarity(vector)


# In[63]:


similarity


# In[64]:


new[new['title'] == 'The Lego Movie'].index[0]


# In[65]:


def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)
        


# In[66]:


recommend('Gandhi')


# In[67]:


import pickle


# In[71]:


pickle.dump(new,open('movie_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




