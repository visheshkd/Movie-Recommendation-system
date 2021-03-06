#pip install rake-nltk

import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

#upload file from local drive....Part 1
import io
from google.colab import files
uploaded = files.upload()
#upload file from local drive....Part 2
df2 = pd.read_csv(io.BytesIO(uploaded['imdb.csv']),error_bad_lines=False)

li = "wordsInTitle,Action,Adult,Adventure,Animation,Biography,Comedy,Crime,Documentary,Drama,Family,Fantasy,FilmNoir,GameShow,History,Horror,Music,Musical,Mystery,News,RealityTV,Romance,SciFi,Short,Sport,TalkShow,Thriller,War,Western"
li = li.split(",")
for i in range(1,len(li)):
  df2[li[i]] = df2[li[i]].replace([0,1],['',li[i]])
df2 = df2[li]
df2['Genre'] = df2[df2.columns[1:]].apply(
    lambda x: ' '.join(x.dropna().astype(str)),
    axis=1
)

# initializing the new column
df2['KeyWords'] = ""

for index, row in df2.iterrows():
    plot = row['Genre']
    
    # instantiating Rake, by default is uses english stopwords from NLTK
    # and discard all puntuation characters
    r = Rake()

    # extracting the words by passing the text
    r.extract_keywords_from_text(plot)

    # getting the dictionary whith key words and their scores
    key_words_dict_scores = r.get_word_degrees()
    
    # assigning the key words to the new column
    row['KeyWords'] = list(key_words_dict_scores.keys())
    
df2.set_index('wordsInTitle', inplace = True)

df2.drop(columns = [col for col in df2.columns if col!= 'Genre'], inplace = True)

# instantiating and generating the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df2['Genre'])

# creating a Series for the movie titles so they are associated to an ordered numerical
# list I will use later to match the indexes
indices = pd.Series(df2.index)

# generating the cosine similarity matrix
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# function that takes in movie title as input and returns the top 10 recommended movies
def recommendations(title, cosine_sim = cosine_sim):
    
    recommended_movies = []
    
    # gettin the index of the movie that matches the title
    idx = indices[indices == title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    
    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_movies.append(list(df2.index)[i])
        
    return recommended_movies

recommendations('into the white')