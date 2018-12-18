import numpy as np
import statsmodels.api as sm

import json
import datetime, time
import collections

hashtags = [ 'nfl', 'superbowl']

for ht in hashtags:
    print ht
    tweets = open(r'C:\Users\Manasi\Documents\Winter2015\ee239\Project 3\tweets_#' + ht + '.txt', 'r')
    line = json.loads(tweets.readline())
    tweets.seek(0, 0)
    start_time = line.get('firstpost_date')

    window = 1 # 1 hour window
    end_time = start_time + window * 3600

    count = []
    number_of_tweets = 0

    for tweet in tweets:

        t = json.loads(tweet)

        if t.get('firstpost_date') < end_time:
            number_of_tweets = number_of_tweets + 1

        else:
            count.append(number_of_tweets)
            end_time = end_time + window * 3600
            number_of_tweets = 0


    print(count)

    print ('############################################')

    sum = 0
    hrcount = 0
    cum_count = []

    for a in count:
        sum = sum + a
        hrcount = hrcount + 1
        cum_count.append(sum/hrcount)

    print (cum_count)

    tweets.close()
