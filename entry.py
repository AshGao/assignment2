#1. Source of Project Gutenberg
import urllib.request

url = 'https://www.gutenberg.org/files/730/730-0.txt'
response = urllib.request.urlopen(url)
data = response.read()  # a `bytes` object
text = data.decode('utf-8')
#print(text) # for testing


#2. Source of Wikipedia
from mediawiki import MediaWiki
wikipedia = MediaWiki()
babson = wikipedia.page("Babson College")
#print(babson.title)
#print(babson.content)

#3. Source of Twitter
# Replace the following strings with your own keys and secrets
import tweepy

TOKEN = 'Your TOKEN'
TOKEN_SECRET = 'Your TOKEN_SECRET'
CONSUMER_KEY = 'Your CONSUMER_KEY'
CONSUMER_SECRET = 'Your CONSUMER_SECRET'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN,TOKEN_SECRET)

api = tweepy.API(auth)

for tweet in api.search_tweets(q="babson college", lang="en", count=10):
    print(f"{tweet.user.name}: {tweet.text}")


#Source of Reddit
import praw
import config
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)
sub = 'learnpython'
submissions = reddit.subreddit(sub).top('day', limit=5)
top5 = [(submission.title, submission.selftext) for submission in submissions]


#Source of Newspaper3
from newspaper import Article

url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
article = Article(url)
article.download()
article.parse()
article.text

