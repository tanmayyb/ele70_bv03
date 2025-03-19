An AnomalyDetection object requires two arguments:
1. csv_data - output dataframe from module 1 (XGBoost) or module 2 (LSTM) that requires the following columns: DateTime, pred, error, {target}
2. target - target label (ex. Toronto, Y_test)

Example usage:
csv_data = pd.read_csv('/content/drive/MyDrive/mcr4_xgb_mt1r1_pred_eval.csv')
anomaly_detection = AnomalyDetection(csv_data, 'Toronto')
anomaly_detection.summary_plots()
anomaly_detection.num_anomalies()
anomaly_detection.best_ten_anomalies()
anomaly_detection.worst_ten_anomalies()
anomaly_detection.anomalies_per_day()
