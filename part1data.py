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



#4. Source of Reddit
import praw
from praw import config
reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     username=config.username,
                     password=config.password,
                     user_agent=config.user_agent)
sub = 'learnpython'
submissions = reddit.subreddit(sub).top('day', limit=5)
top5 = [(submission.title, submission.selftext) for submission in submissions]


#5. Source of Newspaper3
from newspaper import Article

url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
article = Article(url)
article.download()
article.parse()
article.text

#6. Data of Cinemagoer
from imdb import Cinemagoer

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# search movie
movie = ia.search_movie("The Dark Knight")[0]
print(movie.movieID)
# '0468569'

movie_reviews = ia.get_movie_reviews('0468569')
print(movie_reviews['data']['reviews'][0]['content'])

#Pickling Data
import pickle

# Save data to a file (will be part of your data fetching script)
charles_dickens_texts=[]
with open('dickens_texts.pickle','w') as f:
    pickle.dump(charles_dickens_texts,f)


# Load data from a file (will be part of your data processing script)
with open('dickens_texts.pickle','r') as input_file:
    reloaded_copy_of_texts = pickle.load(input_file)




