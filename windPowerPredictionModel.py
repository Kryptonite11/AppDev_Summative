import pandas as pd
import numpy as np
import sys
import pickle

from sklearn.linear_model import LinearRegression # for linear regression modeling
from sklearn import preprocessing # for preprocessing like imputting missing values

from sklearn import metrics


wind_data = pd.read_csv('wind_generation_data.csv')


wind_data = wind_data.fillna(0)

wind_data = wind_data.dropna()
print(wind_data)

X = pd.DataFrame(wind_data.iloc[:,:-1])
y = pd.DataFrame(wind_data.iloc[:,-1])



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=5)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)



regressor = LinearRegression()
regressor.fit(X_train, y_train)


# saving model for later use
filename = 'windMultipleLinearRegressionModel.sav'
pickle.dump(regressor, open(filename, 'wb'))



# ## To load model Later
# # loaded_model = pickle.load(open(filename, 'rb'))
# # result = loaded_model.score(X_test, Y_test)
# # print(result)




v = pd.DataFrame(regressor.coef_, index = ['Co-efficient']).transpose()
w = pd.DataFrame(X.columns, columns = ['Attribute'])

coeff_df = pd.concat([w,v], axis=1, join='inner')
print(coeff_df)

print(X_test)

y_pred = regressor.predict(X_test)
y_pred = pd.DataFrame(y_pred, columns = ['Predicted'])
print(y_pred)


print('Mean absolute error: ', metrics.mean_absolute_error(y_test, y_pred))
print('Mean squared error: ', metrics.mean_squared_error(y_test, y_pred))
print('Root mean squared error: ', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))



