# TWITTER DATA-SCRAPPER

Scrapes the filtered data from Twitter by interative GUI using streamlit.

You can view the App in your browser by clicking the below mentioned link.

https://ajith1046-twitter-scrapper-tweets-4ma4nu.streamlit.app/

SKILLS REQUIRED
1. Python Scripting
2. Snscrape
3. MongoDB
4. Streamlit

PROJECT OVERVIEW:

I have created a streamlit GUI that contains the following features:

1. Any keyword or hashtag to be searched.
2. Select the from and to date.
3. Select the number of tweets to be scraped.

After scraping of tweets,the following actions can be executed:
1. Download the data as CSV file.
2. Download the data as JSON file.
3. View the filtered data in streamlit
4. Upload the data to the database

WORKING:

Step1: Initially, I recieve the Keyword, Start date, End date, and Number of tweets from the user using streamlit.

Step 2: The above details are fed to TwitterSearchScraper and TwitterHashtagScraper. A dataframe is created to store the entire scraped data Now we can download or view this scraped data.

Step3: The database connection is established using pymongo, A new collection will be created and data is uploaded into that collection if the user wish to upload
