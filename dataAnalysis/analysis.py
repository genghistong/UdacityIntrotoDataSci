# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 16:23:59 2014

@author: genghis
"""
import numpy as np
import pandas
import matplotlib.pyplot as plt
import os
import scipy
import scipy.stats
from ggplot import *
import statsmodels.api as sm

os.chdir("/Users/genghis/projects/udacity/dataAnalysis")

def entries_histogram_rain(turnstile_weather):

    fig = plt.figure()
    fig.suptitle('Number of Entries for Rainy Days', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Entries per Hour')
    ax.set_ylabel('Frequency')
    plt.xlim(xmax = 15000)
    turnstile_weather[turnstile_weather['rain'] == 1]['ENTRIESn_hourly'].hist(bins = 100) 
    return plt
    
if __name__ == "__main__":
    image = "withrain.png"
    turnstile_weather = pandas.read_csv("turnstile_data_master_with_weather.csv")
    plt = entries_histogram_rain(turnstile_weather)
    plt.savefig(image)

def entries_histogram_norain(turnstile_weather):

    fig = plt.figure()
    fig.suptitle('Number of Entries for Non-Rainy Days', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Entries per Hour')
    ax.set_ylabel('Frequency')
    plt.ylim(0, 50000)
    plt.xlim(xmax = 15000)
    #plt.ylim(ymax = 50000)
    turnstile_weather[turnstile_weather['rain'] == 0]['ENTRIESn_hourly'].hist(bins = 100) 
    return plt
    
if __name__ == "__main__":
    image = "norain.png"
    turnstile_weather = pandas.read_csv("turnstile_data_master_with_weather.csv")
    plt = entries_histogram_norain(turnstile_weather)
    plt.savefig(image)
    
def KS_test(turnstile_weather):

    with_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1]
    without_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0]
    U, p = scipy.stats.ks_2samp(with_rain, without_rain)
    return U, p # leave this line for the grader


def normalize_features(array):

   array_normalized = (array-array.mean())/array.std()
   mu = array.mean()
   sigma = array.std()

   return array_normalized, mu, sigma

def compute_cost(features, values, theta):
    
    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)
    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):

    m = len(values)
    cost_history = []

    for i in range(num_iterations):
        cost = compute_cost(features, values, theta)
        cost_history.append(cost)
        h = np.dot(features,theta)
        error = values - h
        func = np.dot(error, features)
        theta = theta + (alpha * 1/m * func)
    return theta, pandas.Series(cost_history)

def predictions(dataframe):


    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = dataframe[['fog','EXITSn_hourly','Hour','mintempi','meanpressurei']].join(dummy_units)
    values = dataframe[['ENTRIESn_hourly']]
    m = len(values)

    features, mu, sigma = normalize_features(features)

    features['ones'] = np.ones(m)
    features_array = np.array(features)
    values_array = np.array(values).flatten()

    #Set values for alpha, number of iterations.
    alpha = 0.1 # please feel free to change this value
    num_iterations = 75 # please feel free to change this value

    #Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array, 
                                                            values_array, 
                                                            theta_gradient_descent, 
                                                            alpha, 
                                                            num_iterations)
    

    
    predictions = np.dot(features_array, theta_gradient_descent)
    return predictions, features_array, theta_gradient_descent
    
def compute_r_squared(data, predictions):

    r_squared = 1- ((data - predictions)**2).sum()/((data - np.mean(data))**2).sum()
    return r_squared


if __name__ == "__main__":
    input_filename = "turnstile_data_master_with_weather.csv"
    turnstile_master = pandas.read_csv(input_filename)
    predicted_values = predictions(turnstile_master)
    r_squared = compute_r_squared(turnstile_master['ENTRIESn_hourly'], predicted_values) 

    print r_squared
    print predicted_values
    
def plot_cost_history(alpha, cost_history):

   cost_df = pandas.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
   print ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
      geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )

def plot_residuals(turnstile_weather, predictions):

    fig = plt.figure()
    fig.suptitle('Residuals for Regression', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    ax.set_xlabel('Residuals')
    ax.set_ylabel('Frequency')
    #plt.ylim(0, 3000)
    plt.xlim(xmin = -15000, xmax = 15000)
    (turnstile_weather['ENTRIESn_hourly'] - predictions).hist(bins=100)
    return plt
    
if __name__ == "__main__":
    input_filename = "turnstile_data_master_with_weather.csv"
    turnstile_master = pandas.read_csv(input_filename)
    prediction_values = predictions(turnstile_master)

    image = "residuals.png"
    plt = plot_residuals(turnstile_master, prediction_values)
    plt.savefig(image)
    
def predictions(turnstile_master):
    df = turnstile_master
    df['ones'] = np.ones(( len(df), ))
    Y = df['ENTRIESn_hourly']
    df['UNIT2'] = df['UNIT'].replace('R','')
    df['UNIT2'] = df['UNIT'].map(lambda x: int(x.replace('R', '')))
    
    X = df[['rain','fog','EXITSn_hourly','Hour','mintempi','meanpressurei','UNIT2', 'ones']]
    result = sm.OLS( Y, X ).fit()
    print result.summary()
    prediction = result.predict(X)
    return prediction
