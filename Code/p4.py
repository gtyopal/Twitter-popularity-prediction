import numpy as np
import statsmodels.api as sm
import math
import json
import datetime, time
import collections

f = open(r'C:\Users\Archana\Desktop\Q3\superbowl3.txt', 'r')
l = f.readline()
l = f.readline()
l = f.readline()

l = l.split()
Y = []
X=[map(float,l[x:x+9])for x in xrange(0, len(l), 9)]
results = []

for item in X:
		Y.append(item[1])


split = len(X)/10
print(split)


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
  
