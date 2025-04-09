# Load the datasets API
import urllib.request
api_url = 'https://raw.githubusercontent.com/tanmayyb/ele70_bv03/refs/heads/main/api/datasets.py'
exec(urllib.request.urlopen(api_url).read())

# Train the model and predict the test set
import numpy as np # linear algebra
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd

# def xgb_train(X_train, y_train, X_test, y_test, dt):

#     booster = xgb.XGBRegressor(n_estimators=1000)
#     booster.fit(X_train, y_train,
#             eval_set=[(X_train, y_train), (X_test, y_test)],
#             # early_stopping_rounds=50,
#         verbose=False)
#     pred = booster.predict(X_test)
    
#     output_df = pd.concat([
#         dt, y_test, pd.Series(
#             pred, index=y_test.index, name='pred')],axis=1).dropna()

#     return pred, output_df


def xgb_train(X_train, y_train, X_test, y_test, dt):

    class PlotCallback(xgb.callback.TrainingCallback):
        def __init__(self, update_callback):
            self.update_callback = update_callback

        def before_training(self, model):
            return model

        def after_training(self, model):
            return model

        def after_iteration(self, model, epoch, evals_log):
            # Adjusting for the correct structure:
            train_loss = evals_log.get('train', {}).get('rmse', [None])[epoch]
            val_loss = evals_log.get('eval', {}).get('rmse', [None])[epoch]

            if train_loss is not None and val_loss is not None:
                self.update_callback(train_loss, val_loss)
            # Returning False indicates training should continue
            return False

    class XGBoostTrainer:
        def __init__(self, update_callback):
            """
            Args:
                update_callback: Function that takes (train_loss, val_loss) as arguments.
            """
            self.update_callback = update_callback

        def train(self, X_train, y_train, X_test, y_test):
            dtrain = xgb.DMatrix(X_train, label=y_train)
            dtest = xgb.DMatrix(X_test, label=y_test)

            params = {
                "objective": "reg:squarederror",
                "eval_metric": "rmse",
            }
            evals = [(dtrain, "train"), (dtest, "eval")]

            booster = xgb.train(
                params,
                dtrain,
                num_boost_round=1000,
                evals=evals,
                callbacks=[PlotCallback(self.update_callback)]
            )
            return booster

    # Dummy update function for demonstration:
    def update_plot(train_loss, val_loss):
        # print(f"Train Loss: {train_loss}, Validation Loss: {val_loss}")
        pass

    trainer = XGBoostTrainer(update_plot)
    booster = trainer.train(X_train, y_train, X_test, y_test)

    dtest = xgb.DMatrix(X_test)
    pred = booster.predict(dtest)

    output_df = pd.concat([
        dt, y_test, pd.Series(
            pred, index=y_test.index, name='pred')],axis=1).dropna()

    return pred, output_df