'''
Created on 15.09.2014, edited on 25.11.2014

@author: Esther Seyffarth, edited by Markus Jenning

written in Python 3.3
'''
# coding=utf8


from __future__ import print_function
import tweepy
import time
import config
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re


# Authentication is taken from config.py
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# Establish API session
api = tweepy.API(auth)
# This is your Account name
print(api.me().name)


# Make sure you don't flood the timeline
tweets_count = 0
# Take RE pattern from config.py
pattern = config.pattern


class StdOutListener(StreamListener):
    def on_status(self, status):
        #print(".")
        global tweets_count
        #if tweets_count < 1:
        print(" - ")
        # Make sure the tweet matches the exact RE you defined earlier
        if re.match(pattern, status.text.lower()):
          tweets_count += 1
          #█▓░▒
          try:
            print('░░░░ ',end="")
            print(status.text,end="",flush=True)
            #api.retweet(status.id)
          except UnicodeEncodeError:
            print('▒░▒░',end="")
        else:
          tweets_count += 1
          try:
            print('████ ',end="")
            print(status.text,end="")
          except UnicodeEncodeError:
            print('▒█▒█',end="")
        
        if tweets_count == config.tweets_in_a_row:
            tweets_count = 0
            # Wait specified number of seconds before next RT wave
            time.sleep(config.wait)          
 
    def on_error(self, status):
        # needs better error handling, will crash sooner or later
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    # Search twitter Stream for keywords (no RE search possible)
    stream.filter(track=[config.track])
