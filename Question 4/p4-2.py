import numpy as np
import statsmodels.api as sm
import math
import json
import datetime, time
import collections

#gohawks3
#superbowl3
#nfl3
#patriots3
#sb93
#gopatriots3

f = open(r'C:\Users\Archana\Desktop\Q3\gopatriots3.txt', 'r')
l = f.readline()
l = f.readline()
l = f.readline()


tweets = open(r'C:\Users\Archana\Desktop\UCLA\Quarter2\EE239\tweet_data.tar\tweet_data\\' + 'tweets_#gopatriots.txt', 'r')#sb49
line = json.loads(tweets.readline())
i = 0;
j = 0;
endTime = 0;

# changes for different time periods
for tweet in tweets:
    t = json.loads(tweet)
    if i == 0 : 
        startTime = t.get('firstpost_date')
        i = i +1
     
    if t.get('firstpost_date') > endTime :
        endTime = t.get('firstpost_date')

print(startTime)
print(endTime)     
hours = (endTime-startTime)/3600
print(hours)
print("I",i) 
 
   
l = l.split()
Y = []
print(len(l))
X=[map(float,l[x:x+9])for x in xrange(0, hours, 9)]
results = []

for item in X:
    for itemi in item:
        print(itemi),
    print

print("Length",len(X))
    
for item in X:
	Y.append(item[1])


split = len(X)/10



i = 0
end = split
iValues = []
XTest = []
XTrain = []
YTrain = []
YTest = []
start = 0
end = start+split

while(end<len(X)):
    avgError = 0
    end = start+split
    
    if end > len(X):
        end = len(X)
        
    for x in range(start,end): #1 - 100
        YTest.append(Y[x])
        XTest.append(X[x])
        iValues.append(x)
    
    for x in range(0,len(X)):
        if not x in iValues:
            XTrain.append(X[x])
            YTrain.append(Y[x])
    
   
    YTrain = collections.deque(YTrain)
    YTrain.rotate(-1)
    YTrain = list(YTrain)
    
    res = sm.OLS(YTrain, XTrain).fit()
    results.append(res)
    test_predictions = res.predict(XTest)
     
    for x in range(0,len(YTest)):
        avgError = math.fabs(YTest[x] - test_predictions[x])
        
        
    print(avgError)
    start = end
    XTest = []
    iValues = []
    XTrain = []
    YTrain = []
    YTest = []
              
#print('Standard errors: ', res.bse)
  
