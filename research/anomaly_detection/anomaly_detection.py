import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
import seaborn as sns
from scipy.stats import norm

def anomaly_detection(csv_data, target):

  def statistical_detection(csv_data, num_stds):
    actual = csv_data['Toronto']
    predicted = csv_data['pred']
    errors = csv_data['error']
    data = pd.DataFrame({'Predicted': predicted, 'Actual': actual})

    mean = errors.mean()
    std = errors.std()
    upper_threshold = mean + num_stds * std
    lower_threshold = mean - num_stds * std

    anomalies = data[(errors > upper_threshold) | (errors < lower_threshold)]

    plt.figure(figsize=(10, 6))
    plt.scatter(predicted, actual, label='Normal data', c='blue', alpha=0.7)
    plt.scatter(anomalies['Predicted'], anomalies['Actual'], label='Anomalies', c='red', edgecolors='k')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title(f'Statistical anomaly detection with num_stds={num_stds}')
    plt.legend()
    plt.show()

    return anomalies

  def gmm(csv_data, percentile, prev_anomalies):

    actual = csv_data['Toronto']
    predicted = csv_data['pred']
    errors = csv_data['error'].values.reshape(-1, 1)

    gmm = GaussianMixture(n_components=1, random_state=42).fit(errors)

    log_likelihood = gmm.score_samples(errors)      # how well the model explains observed data
    threshold = np.percentile(log_likelihood, percentile)
    data = pd.DataFrame({'Predicted': predicted, 'Actual': actual})
    anomalies = data[log_likelihood < threshold]

    common_index = anomalies.index.intersection(prev_anomalies.index)
    anomalies = anomalies.loc[common_index]

    p_vals = np.exp(log_likelihood[anomalies.index])
    delta_x = (3.5*errors.std())/(len(errors)**(1/3))
    approx_p = p_vals * delta_x
    norm_scores = 1 - (approx_p - approx_p.min()) / (approx_p.max() - approx_p.min())
    anomalies['Anomaly Score'] = norm_scores

    plt.figure(figsize=(10, 6))
    plt.scatter(predicted, actual, label='Normal data', c='blue', alpha=0.7)
    #plt.scatter(anomalies['Predicted'], anomalies['Actual'], label='Anomalies', c='red', edgecolors='k')
    sc = plt.scatter(anomalies['Predicted'], anomalies['Actual'], c=norm_scores, cmap='viridis', edgecolors='k', s=50, label='Anomalies')
    cbar = plt.colorbar(sc)
    cbar.set_label('Anomaly Likelihood')

    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Final Anomalies')
    plt.legend()
    plt.show()

    return anomalies

  display(csv_data)

  statistical_anomalies = statistical_detection(csv_data, 2)    # approx. 95% of data lies within 2 standard deviations
  print(f'{len(statistical_anomalies)} anomalies detected out of {len(csv_data)} using statistical calculations')

  gmm_anomalies= gmm(csv_data, 5, statistical_anomalies)
  print(f'{len(gmm_anomalies)} final anomalies detected out of {len(csv_data)} using GMM and statistical calculations')
  csv_data['Anomaly Score'] = gmm_anomalies['Anomaly Score']
  worst_ten_idx = gmm_anomalies.sort_values(by=['Anomaly Score'], ascending=False)[0:10].index
  best_ten_idx = gmm_anomalies.sort_values(by=['Anomaly Score'], ascending=True)[0:10].index
  worst_ten_anomalies = csv_data.loc[worst_ten_idx]
  best_ten_anomalies = csv_data.loc[best_ten_idx]
  print('\nWorst ten anomalies')
  display(worst_ten_anomalies[['DateTime', 'Toronto', 'pred', 'Anomaly Score', ]])

  print('\nBest ten anomalies')
  display(best_ten_anomalies[['DateTime', 'Toronto', 'pred', 'Anomaly Score']])

  # find longest streak of consecutive anomalies
  gmm_anomalies['group'] = (gmm_anomalies.index.to_series().diff() != 1).cumsum()
  longest_group = gmm_anomalies['group'].value_counts().idxmax()
  longest_scores = gmm_anomalies[gmm_anomalies['group'] == longest_group]
  longest_scores_idx = longest_scores.index
  consecutive_anomalies = csv_data.loc[longest_scores_idx]
  hours = consecutive_anomalies.index - consecutive_anomalies.index[0]
  consecutive_anomalies['Hour'] = hours

  highest_score_in_streak = consecutive_anomalies.max()['Anomaly Score']
  actual_max = consecutive_anomalies[consecutive_anomalies['Anomaly Score'] == highest_score_in_streak]['Toronto']
  pred_max = consecutive_anomalies[consecutive_anomalies['Anomaly Score'] == highest_score_in_streak]['pred']
  hour_max = consecutive_anomalies[consecutive_anomalies['Anomaly Score'] == highest_score_in_streak]['Hour']
  lowest_score_in_streak= consecutive_anomalies.min()['Anomaly Score']
  actual_min = consecutive_anomalies[consecutive_anomalies['Anomaly Score'] == lowest_score_in_streak]['Toronto']
  pred_min = consecutive_anomalies[consecutive_anomalies['Anomaly Score'] == lowest_score_in_streak]['pred']
  hour_min = consecutive_anomalies[consecutive_anomalies['Anomaly Score'] == lowest_score_in_streak]['Hour']

  plt.figure(figsize=(10, 6))
  plt.plot(hours, consecutive_anomalies['Toronto'], label='Toronto')
  plt.plot(hours, consecutive_anomalies['pred'], label='Predicted')
  plt.plot(hour_max, actual_max, 'bo')
  plt.plot(hour_max, pred_max, 'bo', label='Highest Anomaly Score')
  plt.plot(hour_min, actual_min, 'ro')
  plt.plot(hour_min, pred_min, 'ro', label='Lowest Anomaly Score')
  plt.xticks(consecutive_anomalies['Hour'].unique())
  plt.xlabel('Hour')
  plt.ylabel('Power')
  plt.title(f'Most consecutive anomalies on {consecutive_anomalies["DateTime"][longest_scores_idx[0]][0:10]} from {consecutive_anomalies["DateTime"][longest_scores_idx[0]][11::]}')
  plt.legend()
  plt.show()

  differences = gmm_anomalies.index.to_series().diff()
  max_diff_idx = int(differences.idxmax())
  prev_idx = int(max_diff_idx - differences.loc[max_diff_idx])

  print('\nLongest period without an anomaly:')
  print(f"From {csv_data.loc[prev_idx]['DateTime']} to {csv_data.loc[max_diff_idx]['DateTime']}")

  plt.figure(figsize=(10, 6))
  plt.plot(csv_data.index.to_series()[prev_idx:max_diff_idx+1], csv_data['Toronto'][prev_idx:max_diff_idx+1], label='Actual')
  plt.plot(csv_data.index.to_series()[prev_idx:max_diff_idx+1], csv_data['pred'][prev_idx:max_diff_idx+1], label='Predicted')
  plt.xlabel('Index')
  days = pd.to_datetime(csv_data['DateTime'][prev_idx:max_diff_idx]).dt.day
  plt.ylabel('Power')
  plt.title(f"Longest period without an anomaly: {csv_data.loc[prev_idx]['DateTime']} to {csv_data.loc[max_diff_idx]['DateTime']}")
  plt.legend()
  plt.show()

  anomaly_data = csv_data[csv_data['Anomaly Score'] >= 0]
  month_counts = pd.to_datetime(anomaly_data['DateTime']).dt.month.value_counts()
  plt.figure(figsize=(10, 6))
  plt.bar(month_counts.index, month_counts.values)
  plt.xlabel('Month')
  plt.ylabel('Number of anomalies')
  plt.title('Number of anomalies per month')
  plt.xticks(range(1, 13))
  plt.show()

#csv_data = pd.read_csv('/content/drive/MyDrive/mcr4_xgb_mt1r1_pred_eval.csv')
#anomaly_detection(csv_data, 'Toronto')

#csv_data = pd.read_csv('/content/lstm_Toronto_2.csv')
#anomaly_detection(csv_data, 'Y_test')
