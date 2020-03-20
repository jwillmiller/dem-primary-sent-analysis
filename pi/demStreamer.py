# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Sat Jan 26 17:43:27 2019

@author: willm

Twitter streamer
"""

import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import local_config as lc
import sqlite3
import json

db = "/home/pi/DemData/DemPollingData.db" # database

auth = tweepy.OAuthHandler(lc.consumer_key, lc.consumer_secret)
auth.set_access_token(lc.access_token, lc.access_secret)
api = tweepy.API(auth)

conn = sqlite3.connect(db)
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
c = conn.cursor()

class Tweet():

    # Data on the tweet
    def __init__(self, text, user, followers, date, location):
        self.text = text
        self.user = user
        self.followers = followers
        self.date = date
        self.location = location

    # Inserting that data into the DB
    def insertTweet(self):
        c.execute("INSERT INTO tweets (tweetText, user, followers, date, location) VALUES (?, ?, ?, ?, ?)",
            (self.text, self.user, self.followers, self.date, self.location))
        conn.commit()

# tweepy Listener
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            
            # filter out retweets
            if not tweet['retweeted'] and 'RT @' not in tweet['text']:

                # Get user via Tweepy so we can get their number of followers
                user_profile = api.get_user(tweet['user']['screen_name'])

                # assign all data to Tweet object
                tweet_data = Tweet(
                    str(tweet['text'].encode('utf-8')),
                    tweet['user']['screen_name'],
                    user_profile.followers_count,
                    tweet['created_at'],
                    tweet['user']['location'])

                # Insert that data into the DB
                tweet_data.insertTweet()
                print('success')


            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print('Stream Error: ' + status)
        return True
    
# top 18 candidates as of 9/12
demcandidates = ['Bill de Blasio', 'Steve Bullock', 'Michael Bennet', 'Joe Biden', 'Pete Buttigieg',
                 'Tim Ryan', 'Beto O\'Rourke', 'Bernie Sanders', 'Amy Klobuchar', 'Elizabeth Warren',
                 'Cory Booker', 'Kamala Harris', 'Julian Castro', 'Tulsi Gabbard', 'John Delaney',
                 'Wayne Messam', 'Marianne Williamson', 'Andrew Yang']
        
l = MyListener()
stream = tweepy.Stream(auth, l)
        
stream.filter(track=demcandidates)
