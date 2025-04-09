# Load the datasets API
import urllib.request
api_url = 'https://raw.githubusercontent.com/tanmayyb/ele70_bv03/refs/heads/main/api/datasets.py'
exec(urllib.request.urlopen(api_url).read())

# Train the model and predict the test set
import numpy as np # linear algebra
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error

def xgb_train(X_train, y_train, X_test, y_test):

    booster = xgb.XGBRegressor(n_estimators=1000)
    booster.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            # early_stopping_rounds=50,
        verbose=False)
    pred = booster.predict(X_test)
    
    return pred
