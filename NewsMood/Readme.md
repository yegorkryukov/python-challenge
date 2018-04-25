
## News Mood

In this assignment, you'll create a Python script to perform a sentiment analysis of the Twitter activity of various news oulets, and to present your findings visually.

Your final output should provide a visualized summary of the sentiments expressed in Tweets sent out by the following news organizations: __BBC, CBS, CNN, Fox, and New York times__.

The first plot will be and/or feature the following:

* Be a scatter plot of sentiments of the last __100__ tweets sent out by each news organization, ranging from -1.0 to 1.0, where a score of 0 expresses a neutral sentiment, -1 the most negative sentiment possible, and +1 the most positive sentiment possible.
* Each plot point will reflect the _compound_ sentiment of a tweet.
* Sort each plot point by its relative timestamp.

The second plot will be a bar plot visualizing the _overall_ sentiments of the last 100 tweets from each organization. For this plot, you will again aggregate the compound sentiments analyzed by VADER.

The tools of the trade you will need for your task as a data analyst include the following: tweepy, pandas, matplotlib, seaborn, textblob, and VADER.

Your final Jupyter notebook must:

* Pull last 100 tweets from each outlet.
* Perform a sentiment analysis with the compound, positive, neutral, and negative scoring for each tweet.
* Pull into a DataFrame the tweet's source acount, its text, its date, and its compound, positive, neutral, and negative sentiment scores.
* Export the data in the DataFrame into a CSV file.
* Save PNG images for each plot.

As final considerations:

* Use the Matplotlib and Seaborn libraries.
* Include a written description of three observable trends based on the data.
* Include proper labeling of your plots, including plot titles (with date of analysis) and axes labels.
* Include an exported markdown version of your Notebook called  `README.md` in your GitHub repository.



```python
# Dependencies
import tweepy
import pandas as pd
from pprint import pprint
from config import *
import os
# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import matplotlib.pyplot as plt
import seaborn as sns
#import ast
#from time import sleep
from pprint import pprint
from datetime import datetime

# Twitter API Keys
consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_token_secret = access_token_secret

# Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
```


```python
def rwCSV(path,rw='r',df=None,columns=None):
    '''
    Reads CSV from path to pandas dataframe (rw='r')
    Writes/appends to CSV path from pandas dataframe (rw='w')
    Columns: array-like
    '''
    if rw=='r':
        if os.path.isfile(path): 
            print('rwCSV: returning DF from CSV')
            return pd.read_csv(path)
        else: 
            print(f'rwCSV: returning new DF with columns: {columns}')
            return pd.DataFrame(columns=columns)
    elif rw=='w':
        df = pd.DataFrame(df)
        # if file does not exist write with header 
        if not os.path.isfile(path):
            df.to_csv(path,index=False, columns=columns)
            print(f"rwCSV: saved {df.shape[0]} row(s) as new file to '{path}'")
        else: # else it exists so append without writing the header
            df.to_csv(path,mode = 'a',header=False,index=False, columns=columns)
            print(f"rwCSV: appended {df.shape[0]} row(s) to '{path}'")
```


```python
def getTweets(userName,count=100):
    '''
    gets Tweets from twitter and returns DF
    '''
    #set up resulting columns and DF
    columns = ['account', 'text', 'date', 'compound', 'positive', 'neutral', 'negative']

    tweets_df = pd.DataFrame(columns=columns)

    #get tweets
    try: 
        for status in tweepy.Cursor(api.user_timeline, id=userName).items(count):
            
            #jsonify the response
            tweet = status._json
            
            #extract text
            text = tweet['text']
            
            #analyze text
            result = analyzer.polarity_scores(text)
            
            row = {'account':userName,
                   'text':text,
                   'date':tweet['created_at'],
                   'compound':result['compound'],
                   'positive':result['pos'],
                   'neutral':result['neu'],
                   'negative':result['neg']
                    }
            #grab all the mentions (append to CSV)
            tweets_df = tweets_df.append(row,ignore_index=True)

        
    except tweepy.TweepError as e:
        print(f"getMentions: Something's not right. Error: {e}")
        mention_response = False
    
    tweets_df['date'] = pd.to_datetime(tweets_df['date'])

    return tweets_df
```


```python
#news outlets to analyze
userNames = ['BBC', 'CBS', 'CNN', 'FoxNews', 'nytimes']

#resulting df
tweets = pd.DataFrame()

#how many tweets per outlet to obtain
tweetsPerUser = 100

#obtain tweets and append to resulting DF
for userName in userNames:
    tweets = tweets.append(getTweets(userName,count=tweetsPerUser))

path_to_csv = 'results/tweets.csv'
    
rwCSV(path_to_csv, rw='w', df=tweets)

tweets.head()
```

    rwCSV: saved 500 row(s) as new file to 'results/tweets.csv'





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>account</th>
      <th>text</th>
      <th>date</th>
      <th>compound</th>
      <th>positive</th>
      <th>neutral</th>
      <th>negative</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BBC</td>
      <td>In 1941, Josef Jakobs was executed at the Towe...</td>
      <td>2018-04-25 20:12:00</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BBC</td>
      <td>Hugh Fearnley-Whittingstall is on a mission, a...</td>
      <td>2018-04-25 19:03:06</td>
      <td>-0.1779</td>
      <td>0.000</td>
      <td>0.898</td>
      <td>0.102</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BBC</td>
      <td>☀️🛶 How an isolated indigenous community in Ec...</td>
      <td>2018-04-25 18:00:25</td>
      <td>-0.1531</td>
      <td>0.077</td>
      <td>0.818</td>
      <td>0.105</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BBC</td>
      <td>🌱🍓 A man has told of how he 'got his mum back'...</td>
      <td>2018-04-25 17:01:10</td>
      <td>0.0000</td>
      <td>0.000</td>
      <td>1.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BBC</td>
      <td>❤️🐿 The dating scene is tough when you're a re...</td>
      <td>2018-04-25 16:00:21</td>
      <td>-0.1280</td>
      <td>0.000</td>
      <td>0.870</td>
      <td>0.130</td>
    </tr>
  </tbody>
</table>
</div>




```python
#plot scatter
#setup save path    
path = 'results/image_all_news_scatter.png'

#group by account for plotting
df = tweets.groupby(['account'])['compound']

#plot
plt.style.use('fivethirtyeight')
f, ax = plt.subplots(figsize=(20,10))
df.plot(marker='o',linewidth=0,ax=ax)
plt.legend(loc='center', bbox_to_anchor=(1.05, 0.5), shadow=False, ncol=1,title='News outlets:')
plt.gca().invert_xaxis() #invert x axis so latest tweets are on the right
plt.xlim([tweetsPerUser-0.5,0-.5]) #setup limits so scatter marker is not cut by outer lines
plt.ylim(-1,1) #setup y lims per possible compound limits 
plt.ylabel("Tweet polarity \n<negative.........positive>")
plt.xlabel("Tweets Ago")
now = datetime.now()
now = now.strftime("%m/%d/%Y")
plt.title(f"Sentiment analysis of News outlet tweets as of {now}")
plt.savefig(path, format='png',dpi=150,transparent=True,bbox_inches='tight')
plt.show(f)
```


![png](output_5_0.png)



```python
#plot bar
#setup save path    
path = 'results/image_all_news_bar.png'

#group by account for plotting
df = tweets.groupby(['account']).agg({'compound':'mean'})

#plot
plt.style.use('fivethirtyeight')
f, ax = plt.subplots(figsize=(20,10))
df['compound'].plot(kind='bar')
plt.xticks(rotation=0)
plt.ylabel("Tweet polarity \n<negative.........positive>")
plt.xlabel('')
now = datetime.now()
now = now.strftime("%m/%d/%Y")
plt.title(f"Overal media sentiment on Twitter as of {now}")
plt.savefig(path, format='png',dpi=150,transparent=True,bbox_inches='tight')
plt.show(f)
```


![png](output_6_0.png)


## Observations
1. It is really hard to make anything out of the first plot
2. It seems like CBS's wording makes Vader think it's more positive
3. Based on my experience working with Vader any conclusions has to be made after much thorough analysis than this one
