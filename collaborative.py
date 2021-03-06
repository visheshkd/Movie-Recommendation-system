import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')
#Uploading file from local drive
import io
from google.colab import files
uploaded = files.upload()
#Uploading the user ratings of the movies for collaborative filtering , recommending movies using the ratings of movies given by each user
movie_ratings = pd.read_csv(io.BytesIO(uploaded['ratings.csv']),error_bad_lines=False)

import io
from google.colab import files
uploaded = files.upload()
#Uploading movie names now.
movie_names = pd.read_csv(io.BytesIO(uploaded['movies.csv']),error_bad_lines=False)
#movie_names.head() - head to see how the dataset looks like.

df = pd.merge(movie_ratings, movie_names, on='movieId') # Merging the movie names and movie ratings
ratings = pd.DataFrame(df.groupby('title')['rating'].mean()) #creating a dataframe using pandas , getting the average of ratings(user-given) for each movie 
ratings['rate_counts'] = df.groupby('title')['rating'].count() #here getting the number of rate counts for each particular movie
movie_matrix = df.pivot_table(index='userId', columns='title', values='rating')
#matrix --> [row,col]=[user_id, movie_titles],matrix_values=movie_ratings
#collaborative approach --> item-item similarity
movie_user_rating = movie_matrix['Star Trek: Generations (1994)']#recommending movies with respect to user current watch history(movie name) and user_ratings.
# Here, using Pearson correlation coefficient for giving proper recommendation of movies.
movie_similarity=movie_matrix.corrwith(movie_user_rating)#correlation coefficient value range is (-1 to 1)
#Correlation --> required - Strong or moderate degree(atleast) : >0.30 , close to 0 means two movies can be related non-linearly and less than 0 is negative relation.
correlate = pd.DataFrame(movie_similarity, columns=['correlation_coeff'])
correlate.dropna(inplace=True)#dropping the null values using dropna function
correlate = correlate.join(ratings['rate_counts'])
#Calculating the root mean square error and finding the accuracy of the model , which varies with respect to the number of ratings threshold.
n = 10
acc = correlate[correlate['rate_counts'] > 100].sort_values(by='correlation_coeff', ascending=False).head(n) # given threshold, sorting in descending order to get top 10 recommendations
ls = []
sum = 0
count = 0
for i in range(0,n):
  temp = (acc['correlation_coeff'][i])
  '''
  if(temp > 0.5):
    sum = sum + np.square(1-temp)
  else:
    sum = sum + np.square(0.5-temp)
  '''
  if(temp < 0.5):
    sum = sum + np.square(0.5-temp)
    count += 1
#mse = sum/n 
if count == 0 and sum == 0:
  mse = 0
  rmse = 0
else:
  mse = sum/count
  rmse = np.sqrt(mse)
accuracy_mse = (1-mse)*100
accuracy_rmse = (1-rmse)*100
print("Recommended Movies:\n")
print(acc)
print("*******************************************")
#print("Accuracy MSE:", accuracy_mse)
print("Accuracy RMSE:", accuracy_rmse)