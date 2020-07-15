import tweepy
from textblob import TextBlob
from csv import writer

consumer_key = 'skrrhvZmeKNuZvI0Z1sGgWQMJ'
consumer_key_secret = 'RkFVEBn66lianCo1XgmxJohHQXbtkgrrPQ9KejqrU5MnVLs8b5'

access_token = '2261270106-vrPqTCE3iFNi6rGwUUQAhFYMLH1xXbxrgTWuumw'
access_token_secret = 'd0fVkCHnChJFaYnt0eyuuCblpjACdBxemVsIi6vuwo7tf'

#positive = 1
#neutral = 0
#negative = -1

num_tweets = 0
num_positive_tweets = 0
num_negative_tweets = 0
num_neutral_tweets = 0

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

keywords = ["#coronavirus", "#lockdown", "#coronaupdatesindia", "#coronavirusindia"]

with open("tweet_data.csv", "w", encoding="utf-8") as file:
		csv_writer = writer(file)
		csv_writer.writerow(["Tweet Number", "Tweet","Tweet Polarity", "Tweet Subjectivity", "Result", "Num Positive Tweets", "Num Negative Tweets", "Num Neutral Tweets", "Positive Percentage", "Negative Percentage", "Neutral Percentage"])

def get_tweets(keyword):
	with open("tweet_data.csv", "a", encoding="utf-8") as file:
		csv_writer = writer(file)
		for tweet in tweepy.Cursor(api.search,q=keyword + " -filter:retweets",lang = "en", geocode='20.5936832,78.962883,10000km').items(200):
			print(tweet.text)
			global num_tweets
			global num_positive_tweets 
			global num_negative_tweets 
			global num_neutral_tweets
			num_tweets += 1
			analysis = TextBlob(tweet.text)
			print(analysis.noun_phrases)
			if analysis.sentiment[0]>0:
				num_positive_tweets += 1
				csv_writer.writerow([num_tweets, tweet.text, analysis.sentiment[0], analysis.sentiment[1], "Positive", num_positive_tweets, num_negative_tweets, num_neutral_tweets])
			elif analysis.sentiment[0]<0:
				num_negative_tweets += 1
				csv_writer.writerow([num_tweets, tweet.text, analysis.sentiment[0], analysis.sentiment[1], "Negative", num_positive_tweets, num_negative_tweets, num_neutral_tweets])
			else:
				num_neutral_tweets += 1
				csv_writer.writerow([num_tweets, tweet.text, analysis.sentiment[0], analysis.sentiment[1], "Neutral", num_positive_tweets, num_negative_tweets, num_neutral_tweets])

for keyword in keywords:
	get_tweets(keyword)

print(f"Total Tweets: {num_tweets}\nPositive Tweets: {num_positive_tweets}\nNegative Tweets: {num_negative_tweets}\nNeutral Tweets: {num_neutral_tweets}")
positive_percentage = (num_positive_tweets/num_tweets) * 100
negative_percentage = (num_negative_tweets/num_tweets) * 100
neutral_percentage = (num_neutral_tweets/num_tweets) * 100
with open("tweet_data.csv", "a", encoding="utf-8") as file:
		csv_writer = writer(file)
		csv_writer.writerow(["Summary","","","","","","","",f"{positive_percentage}", f"{negative_percentage}", f"{neutral_percentage}"])
