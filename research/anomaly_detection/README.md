Anomaly detection takes two arguments:
1. csv_data - output dataframe from module 1 (XGBoost) or module 2 (LSTM) that requires the following columns: DateTime, pred, error, {target}
2. target - target label (ex. Toronto, Y_test)

Example run command: anomaly_detection("XGBoost_data.csv", Toronto)
