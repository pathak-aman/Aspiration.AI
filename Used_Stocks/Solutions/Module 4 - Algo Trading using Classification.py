
# coding: utf-8

# # Module 4 - Algo Trading using Classification
# 

#    ### Welcome to the Answer notebook for Module 4 ! 
# Make sure that you've submitted the module 3 notebook and unlocked Module 4 yourself before you start coding here
# 

# #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# ### Query 4.1 
# Import the csv file of the stock which contained the Bollinger columns as well.
# 
# 

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression  
from sklearn import svm,preprocessing
from sklearn.ensemble import RandomForestClassifier


tcs_dat = pd.read_csv('tcs_stock_data.csv')


# In[ ]:


tcs_dat['14 Day MA'] = tcs_dat['Close Price'].rolling(window=14).mean()
tcs_dat['30 Day STD'] = tcs_dat['Close Price'].rolling(window=20).std()
tcs_dat['Upper Band'] = tcs_dat['14 Day MA'] + (tcs_dat['30 Day STD'] * 2)
tcs_dat['Lower Band'] = tcs_dat['14 Day MA'] - (tcs_dat['30 Day STD'] * 2)
tcs_dat = tcs_dat.dropna()
tcs_dat['Mid Band'] = (tcs_dat['Upper Band']+tcs_dat['Lower Band'])/2


# ### Query 4.1a 
# 
# Create a new column 'Call' , whose entries are - 
# 
# >'Buy' if the stock price is below the lower Bollinger band 
# 
# >'Hold Buy/ Liquidate Short' if the stock price is between the lower and middle Bollinger band 
# 
# >'Hold Short/ Liquidate Buy' if the stock price is between the middle and upper Bollinger band 
# 
# >'Short' if the stock price is above the upper Bollinger band
# 
# 
# 

# In[ ]:


def select_buy(tcs_dat):
    if tcs_dat['Close Price'] < tcs_dat['Lower Band']:
        return "Buy"
    if tcs_dat['Close Price'] > tcs_dat['Lower Band'] and tcs_dat['Close Price'] < tcs_dat['Mid Band']:
        return "Hold Buy/ Liquidate Short"
    if tcs_dat['Close Price'] > tcs_dat['Mid Band'] and tcs_dat['Close Price'] < tcs_dat['Upper Band']:
        return "Hold Short/ Liquidate Buy"
    if tcs_dat['Close Price'] > tcs_dat['Upper Band']:
        return "Short"
tcs_dat = tcs_dat.assign(Call = tcs_dat.apply(select_buy, axis=1))


# ### Query 4.1b
# Now train a classification model with the 3 bollinger columns and the stock price as inputs and 'Calls' as output. Check the accuracy on a test set. (There are many classifier models to choose from, try each one out and compare the accuracy for each)
# Import another stock data and create the bollinger columns. Using the already defined model, predict the daily calls for this new stock.

# In[ ]:


le = preprocessing.LabelEncoder()
train_X = tcs_dat[['Upper Band','Lower Band','Mid Band','Close Price']]
transfomed_label = le.fit_transform(tcs_dat[['Call']])
train_Y = transfomed_label.reshape(-1,1)


# In[ ]:


LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr').fit(train_X, train_Y.ravel())
LR.predict(train_X) 
print("Logistic Regression")
print(round(LR.score(train_X,train_Y),4))


# In[ ]:


SVM = svm.LinearSVC()
SVM.fit(train_X, train_Y)
SVM.predict(train_X)
print("Support Vector Machines")
print(round(SVM.score(train_X,train_Y), 4))


# ### Query 4.2
# Now, we'll again utilize classification to make a trade call, and measure the efficiency of our trading algorithm over the past two years. For this assignment , we will use RandomForest classifier.
# Import the stock data file of your choice
# Define 4 new columns , whose values are: 
# % change between Open and Close price for the day 
# % change between Low and High price for the day 
# 5 day rolling mean of the day to day % change in Close Price 
# 5 day rolling std of the day to day % change in Close Price
# Create a new column 'Action' whose values are: 
# 1 if next day's price(Close) is greater than present day's. 
# (-1) if next day's price(Close) is less than present day's. 
# i.e. Action [ i ] = 1 if Close[ i+1 ] > Close[ i ] 
# i.e. Action [ i ] = (-1) if Close[ i+1 ] < Close[ i ]
# Construct a classification model with the 4 new inputs and 'Action' as target
# Check the accuracy of this model , also , plot the net cumulative returns (in %) if we were to follow this algorithmic model
# 

# In[ ]:


wipro_data = pd.read_csv('wipro_stock_data.csv')
wipro_data['%chg op_cl'] = ((wipro_data['Close Price'] - wipro_data ['Open Price'])/(wipro_data['Close Price']))*100
wipro_data['%chg lw_hg'] = ((wipro_data['Close Price'] - wipro_data ['High Price'])/(wipro_data['Low Price']))*100
wipro_data['%chg 5dymean'] = wipro_data['Close Price'].pct_change().dropna().rolling(5).mean()
wipro_data['%chg 5dystd'] = wipro_data['Close Price'].pct_change().dropna().rolling(5).std()
wipro_data = wipro_data.dropna()

arr = []
val = []
for value in wipro_data['Close Price'].iteritems():
    arr.append(value[1])
for i in range(0,483):
    if arr[i+1] > arr[i]:
        val.append(1)
    else:
        val.append(-1)
wipro_data['Action'] = pd.DataFrame(val)
wipro_data = wipro_data.dropna()


train_X = wipro_data[['%chg op_cl','%chg lw_hg','%chg 5dymean','%chg 5dystd']]
train_Y = wipro_data[['Action']]

RF = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)  
RF.fit(train_X, train_Y)  
RF.predict(train_X) 
print("Random Forests")
round(RF.score(train_X,train_Y), 4) 
wipro_data['Net Cummulative Returns'] = (((wipro_data['Open Price'] - wipro_data['Close Price'])/(wipro_data['Open Price']))*100).cumsum()
plt.figure(figsize=(20,10))
plt.plot(wipro_data['Net Cummulative Returns'])

