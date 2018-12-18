import json
import datetime, time

hashtags = ['gohawks' , 'gopatriots' , 'nfl', 'patriots' , 'sb49', 'superbowl']

for ht in hashtags:
    tweets = open(r'C:\Users\Mukti Desai\Dropbox\Masters\Winter Quarter\EE239AS\#3\tweet_data\tweets_#' + ht + '.txt', 'r')
    line = json.loads(tweets.readline())
    tweets.seek(0, 0)
    start_time = line.get('firstpost_date')
    number_of_tweets = 0
    end_time = 0

    user_ids = []
    no_of_followers = []
    user_ids.append(line.get('tweet').get('user').get('id'))
    no_of_followers.append(line.get('tweet').get('user').get('followers_count'))
    
    no_of_retweets = 0
    
    for tweet in tweets:
        t = json.loads(tweet)
        number_of_tweets = number_of_tweets + 1
        end_time = t.get('firstpost_date')
        user_id = t.get('tweet').get('user').get('id')
        number_of_followers = t.get('tweet').get('user').get('followers_count')
        if user_id not in user_ids:
            user_ids.append(user_id)
            no_of_followers.append(number_of_followers)
        else:
            no_of_followers[user_ids.index(user_id)] = number_of_followers

        #no_of_retweets = no_of_retweets + t.get('metrics').get('citations').get('data')[-1].get('citations')
        no_of_retweets = no_of_retweets + t.get('metrics').get('citations').get('total')
        #print ('*')

                
    print number_of_tweets/((end_time - start_time)/3600)
    print sum(no_of_followers)/len(user_ids)
    print no_of_retweets/number_of_tweets
    tweets.close()
