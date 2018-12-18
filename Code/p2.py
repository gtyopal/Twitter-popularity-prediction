import numpy as np
import statsmodels.api as sm

import json
import datetime, time
import collections

hashtags = ['gohawks' , 'gopatriots' , 'nfl', 'patriots' , 'sb49', 'superbowl']
#hashtags = ['gopatriots']
results = []
for ht in hashtags:
    print ht
    tweets = open(r'C:\Users\Manasi\Documents\Winter2015\ee239\Project 3\tweets_#' + ht + '.txt', 'r')
    line = json.loads(tweets.readline())
    tweets.seek(0, 0)
    start_time = line.get('firstpost_date')

    number_of_tweets = 0
    number_of_retweets = 0
    number_of_followers = 0
    max_followers = 0
    
    window = 1 # 1 hour window
    end_time = start_time + window * 3600

    X = []
    Xi = [] # i => ith window
    Xi.append(1)

    Y = []
        
    for tweet in tweets:
        t = json.loads(tweet)
        if t.get('firstpost_date') < end_time:
            number_of_tweets = number_of_tweets + 1
            number_of_retweets = number_of_retweets + t.get('metrics').get('citations').get('total')
            number_of_followers = number_of_followers + t.get('tweet').get('user').get('followers_count')
            if t.get('tweet').get('user').get('followers_count') > max_followers:
                max_followers = t.get('tweet').get('user').get('followers_count')
        else:
            Xi.append(number_of_tweets)
            Y.append(number_of_tweets)
            number_of_tweets = 1
            
            Xi.append(number_of_retweets)
            number_of_retweets = t.get('metrics').get('citations').get('total')

            Xi.append(number_of_followers)
            number_of_followers = t.get('tweet').get('user').get('followers_count')

            Xi.append(max_followers)
            max_followers = t.get('tweet').get('user').get('followers_count')

            Xi.append(int(datetime.datetime.fromtimestamp(t.get('firstpost_date')).strftime("%H")))
            end_time = end_time + window * 3600

            X.append(Xi)
            Xi = []
            Xi.append(1)
        
    Y = collections.deque(Y)
    Y.rotate(-1)
    Y = list(Y)
    
    #X = sm.add_constant(X)
    res = sm.OLS(Y, X).fit()
    results.append(res)
    
    print('Parameters: ', res.params)
    print('Standard errors: ', res.bse)
    print('Predicted values: ', res.predict())

    print('t_test: ', res.t_test)
    print('p values: ', res.pvalues)
    print('t values', res.tvalues)

    tweets.close()
