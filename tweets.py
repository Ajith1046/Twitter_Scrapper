# Importing the necessary modules for this project

import snscrape.modules.twitter as sntwitter
import datetime as datetime
import pymongo
import pandas as pd
import streamlit as st
import time


# Assigning the required variables
tweet_list = []
tweet_df = pd.DataFrame()

# Setting up a UI using streamlit
st.write("# Twitter Data-Scrapper ")
option = st.selectbox('How do you want to scrape the data?', ('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'twitter')
start_date = st.date_input("Select the Start Date", datetime.date(2019, 12, 10), key='d1')
end_date = st.date_input("Select the End Date", datetime.date(2023, 1, 1), key='d2')
tweet_limit = st.slider('Number of tweets to be scraped', 0, 1000, 10)

# Connect to MongoDb and create a database
client_url = "mongodb+srv://ajithh10:Ajith.h98@tweets.ma9kp8t.mongodb.net/test"
client = pymongo.MongoClient(client_url)
myDB = client["Twitter_database"]


# Scrape the tweets using snscrape

if word:
    if option == 'keyword':
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start_date} until:{end_date}').get_items()):
            if i >= tweet_limit:
                break
            else:
                tweet_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])
        tweet_df = pd.DataFrame(tweet_list, columns=['ID', 'Date', 'Content', 'Language', 'Username', 'Replycount', 'Retweetcount', 'Likecount', 'Source', 'Url'])
    else:
        for i, tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start_date} until:{end_date}').get_items()):
            if i >= tweet_limit:
                break
            else:
                tweet_list.append([tweet.id, tweet.date, tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.source, tweet.url])
        tweet_df = pd.DataFrame(tweet_list, columns=['ID', 'Date', 'Content', 'Language', 'Username', 'Replycount', 'Retweetcount', 'Likecount', 'Source', 'Url'])
else:
    st.warning(option, 'cannot be empty', icon='🚨')

# Cache the conversion to prevent commutation
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

if not tweet_df.empty:
    col1, col2, col3, col4 = st.columns(4)

    with col1:  # Download data as CSV file
        csv = convert_df(tweet_df)
        a = st.download_button(label='Download data as CSV', data=csv, file_name='Twitter_scrape.csv', mime='text/csv')
    with col2:  # Download data as JSON file
        json = tweet_df.to_json(orient='records')
        b = st.download_button(label='Download data as JSON file', data=json, file_name='Twitter_scrape.json', mime='application/json')
    with col3:  # Show the filtered tweets
        c = st.button('Show filtered tweets', key=2)
    with col4:  # Upload the data to database
        d = st.button('Upload tweets to database', key=3)

if a:
    st.success('The scraped data is successfully downloaded as CSV file', icon='✅')

if b:
    st.success('The scraped data is successfully downloaded as JSON file', icon='✅')

if c:
    st.success('Tweets are scraped successfully', icon='✅')
    st.dataframe(tweet_df)

if d:
       # Upload data to database in MongoDB
    coll = word
    coll = coll.replace(' ', '_')+'_Tweets'
    mycoll = myDB[coll]
    dict1 = tweet_df.to_dict('records')
    if dict1:
        mycoll.insert_many(dict1)
        ts = time.time()
        mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
        st.success('Successfully uploaded to database', icon="✅")
    else:
        st.warning('Could not upload data because there are no tweets', icon="⚠")
