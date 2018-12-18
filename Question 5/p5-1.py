import numpy as np
import statsmodels.api as sm

import json
import datetime, time
import collections

#hashtags = ['gohawks' , 'gopatriots' , 'nfl', 'patriots' , 'sb49', 'superbowl']
hashtags = ['gohawks' , 'gopatriots']
results = []
for ht in hashtags:
    print ht
    tweets = open(r'C:\Users\Archana\Desktop\UCLA\Quarter2\EE239\test_data\\' + 'sample5_period2.txt' + ht + '.txt', 'r')
    line = json.loads(tweets.readline())
    tweets.seek(0, 0)
    start_time = line.get('firstpost_date')

    #1 : Total number of tweets
    number_of_tweets = 0

    #2 : Total number of citations
    number_of_citations = 0

    #3 : Total number of followers
    number_of_followers = 0

    #4 : Maximum number of followers
    max_followers = 0    

    #5 : Total number of impressions
    impressions_count = 0
        
    #6 : Total unique Author Count
    authors = []

    #7 : URL Ratio
    url_ratio = 0

    #8 : Total Ranking Score
    ranking_score = 0

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
            number_of_citations = number_of_citations + t.get('metrics').get('citations').get('total')
            number_of_followers = number_of_followers + t.get('tweet').get('user').get('followers_count')
            if t.get('tweet').get('user').get('followers_count') > max_followers:
                max_followers = t.get('tweet').get('user').get('followers_count')
            impressions_count = impressions_count + t.get('metrics').get('impressions')
            if t.get('original_author').get('url') not in authors:
                authors.append(t.get('original_author').get('url'))
            if t.get('tweet').get('entities').get('urls'):
                url_ratio = url_ratio + 1
            ranking_score = ranking_score + t.get('metrics').get('ranking_score')
        else:
            Xi.append(number_of_tweets)
                        
            Xi.append(number_of_citations)
            number_of_citations = t.get('metrics').get('citations').get('total')

            Xi.append(number_of_followers)
            number_of_followers = t.get('tweet').get('user').get('followers_count')

            Xi.append(max_followers)
            max_followers = t.get('tweet').get('user').get('followers_count')

            Xi.append(impressions_count)
            impressions_count = t.get('metrics').get('impressions')
            
            Xi.append(len(authors))
            authors = []

            url_ratio = float(url_ratio)/number_of_tweets
            Xi.append(url_ratio)
            if t.get('tweet').get('entities').get('urls'):
                url_ratio = 1
            else:
                url_ratio = 0
            
            Xi.append(ranking_score)
            ranking_score = t.get('metrics').get('ranking_score')
            end_time = start_time + window * 3600
            Y.append(number_of_tweets)
            number_of_tweets = 1

            X.append(Xi)
            Xi = []
            Xi.append(1)
        
    Y = collections.deque(Y)
    Y.rotate(-1)
    Y = list(Y)
    
    #X = sm.add_constant(X)
    res = sm.OLS(Y, X).fit()
    results.append(res)
    
    for item in X:
        for itemi in item:
            print itemi,
        print
        
    
    print('Summary: ', res.summary)
    print('Parameters: ', res.params)
    print('Standard errors: ', res.bse)
    print('Predicted values: ', res.predict())
    print('Accuracy :', res.rsquared)
    print('t values', res.tvalues)
    print('p values: ', res.pvalues)
    
    
    tweets.close()
