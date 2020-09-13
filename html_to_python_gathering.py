#!/usr/bin/env python
# coding: utf-8

# ## Quiz - HTML Files in Python
# 
# With your knowledge of HTML file structure, we're going to use Beautiful Soup to extract our desired Audience Score metric and number of audience ratings, along with the movie title like in the video above (so we have something to merge the datasets on later) for each HTML file, then save them in a pandas DataFrame.
# 
# The Jupyter Notebook below contains template code that:
# 
# - Creates an empty list, df_list, to which dictionaries will be appended. This list of dictionaries will eventually be converted to a pandas DataFrame (this is the most efficient way of building a DataFrame row by row).
# - Loops through each movie's Rotten Tomatoes HTML file in the rt_html folder.
# - Opens each HTML file and passes it into a file handle called file.
# - Creates a DataFrame called df by converting df_list using the pd.DataFrame constructor.
# 
# Your task is to extract the title, audience score, and number of audience ratings in each HTML file so each trio can be appended as a dictionary to df_list.
# 
# The Beautiful Soup methods required for this task are:
# 
# - find()
# - find_all()
# 
# There is an excellent tutorial on these methods (Searching the tree) in the Beautiful Soup documentation. Please consult that tutorial if you are stuck.

# In[1]:


from bs4 import BeautifulSoup
import os
import pandas as pd


# In[2]:


# List of dictionaries to build file by file and later convert to a DataFrame
df_list = []
folder = 'rt_html'
for movie_html in os.listdir(folder):
    with open(os.path.join(folder, movie_html)) as file:
        soup = BeautifulSoup(file, 'lxml')
        title = soup.find('title').contents[0][:-len(' - Rotten Tomatoes')]
        audience_score = soup.find('div', class_='audience-score meter').find('span').contents[0][:-1]
        num_audience_ratings = soup.find('div', class_="audience-info hidden-xs superPageFontColor")
        num_audience_ratings = num_audience_ratings.find_all('div')[1].contents[2].strip().replace(',','')
        # Append to list of dictionaries
        df_list.append({'title': title,
                        'audience_score': int(audience_score),
                        'number_of_audience_ratings': int(num_audience_ratings)})
df = pd.DataFrame(df_list, columns = ['title', 'audience_score', 'number_of_audience_ratings'])


# In[3]:


df


# ## Solution Test
# Run the cell below the see if your solution is correct. If an `AssertionError` is thrown, your solution is incorrect. If no error is thrown, your solution is correct.

# In[4]:


df_solution = pd.read_pickle('df_solution.pkl')
df.sort_values('title', inplace = True)
df.reset_index(inplace = True, drop = True)
df_solution.sort_values('title', inplace = True)
df_solution.reset_index(inplace = True, drop = True)
pd.testing.assert_frame_equal(df, df_solution)

