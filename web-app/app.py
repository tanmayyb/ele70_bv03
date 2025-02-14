# app.py

from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import numpy as np
import xgboost as xgb
import os
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI environments
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
from plotly.offline import plot

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your secret key

# Hardcoded user credentials (for demonstration)
USERNAME = 'admin'
PASSWORD = 'password'

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

# Preprocess function (as per your notebook)
def preprocess(dataset: pd.DataFrame, split_datetime=True):
    df = dataset.copy()
    ieso_cols = ['Toronto']
    climate_cols = [
        'Temp (°C)',
        'Dew Point Temp (°C)',
        'Rel Hum (%)',
        'Precip. Amount (mm)',
        'Stn Press (kPa)',
        'Hmdx',
    ]
    if split_datetime:
        df['Y'] = pd.to_datetime(df['DateTime']).dt.year
        df['M'] = pd.to_datetime(df['DateTime']).dt.month
        df['D'] = pd.to_datetime(df['DateTime']).dt.day
        df['H'] = pd.to_datetime(df['DateTime']).dt.hour
        cols = ['Y', 'M', 'D', 'H']
    else:
        cols = ['DateTime']

    # Delete leap day
    df = df[~((pd.to_datetime(df['DateTime']).dt.month == 2) & (pd.to_datetime(df['DateTime']).dt.day == 29))]
    dt = pd.to_datetime(df['DateTime'])

    cols += ieso_cols + climate_cols
    df = df[cols]

    # Clean column names
    df.columns = df.columns.str.replace('.', '', regex=False)
    df.columns = df.columns.str.replace(' ', '', regex=False)
    df.columns = df.columns.str.replace(r"\(.*?\)", "", regex=True)

    # Handle missing values
    df = df.fillna(df.mean())

    return df, dt

# Function to create train-test split
def create_train_test_split(dataset: pd.DataFrame, target: str = 'Toronto', split_coeff: float = 0.8, dt=None):
    training_cutoff = int(split_coeff * len(dataset))
    train = dataset.iloc[:training_cutoff]
    test = dataset.iloc[training_cutoff:]

    X_train = train.drop(columns=[target])
    y_train = train[target]
    X_test = test.drop(columns=[target])
    y_test = test[target]

    (train_idx, test_idx) = None, None
    if dt is not None:
        train_idx = dt.iloc[:training_cutoff]
        test_idx = dt.iloc[training_cutoff:]

    return (X_train, X_test, y_train, y_test), (train_idx, test_idx)

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload_file'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Route for the file upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part.'
            return render_template('upload.html', error=error)
        file = request.files['file']
        if file.filename == '':
            error = 'No selected file.'
            return render_template('upload.html', error=error)
        if file and allowed_file(file.filename):
            filename = 'uploaded_data.csv'
            filepath = os.path.join('uploads', filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(filepath)
            session['uploaded_file'] = filepath
            return redirect(url_for('model_selection'))
        else:
            error = 'Invalid file type. Please upload a CSV file.'
            return render_template('upload.html', error=error)
    return render_template('upload.html')

# Route for the model selection page
@app.route('/models', methods=['GET', 'POST'])
def model_selection():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        model_choice = request.form['model']
        session['model_choice'] = model_choice
        return redirect(url_for('display_graph'))
    return render_template('models.html')

# Route for displaying the graph
@app.route('/graph')
def display_graph():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    uploaded_file = session.get('uploaded_file')
    if not uploaded_file or not os.path.exists(uploaded_file):
        return redirect(url_for('upload_file'))

    # Read the uploaded CSV file
    dataset = pd.read_csv(uploaded_file)

    # Preprocess the dataset
    df, dt = preprocess(dataset)

    # Create train-test split
    target = 'Toronto'
    (X_train, X_test, y_train, y_test), (train_idx, test_idx) = create_train_test_split(df, target=target, dt=dt)

    # Train the model
    reg = xgb.XGBRegressor(n_estimators=1000)
    reg.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    # Make predictions
    pred = reg.predict(X_test)

    # Create the plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test_idx, y=y_test.to_numpy(), mode='lines', name='Actual', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=test_idx, y=pred, mode='lines', name='Predicted', line=dict(color='red')))

    fig.update_layout(
        title=f"Time Series Forecasting for {target} with XGBoostRegressor",
        xaxis_title="DateTime",
        yaxis_title="Energy Demand",
        template="plotly_dark"
    )

    # Generate the HTML div with the plot
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    return render_template('graph.html', plot_div=plot_div)

# Helper route to handle logout (optional)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Ensure the 'uploads' directory exists
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
