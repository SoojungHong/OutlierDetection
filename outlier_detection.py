# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 16:34:31 2017

@author: a613274

@about: Outlier detection 
@reference:  
"""

#-----------------------
# Import Libraries 
#-----------------------
import matplotlib.pyplot as plt
import numpy as np

from numpy import genfromtxt
from scipy.stats import multivariate_normal
from sklearn.metrics import f1_score

def read_dataset(filePath, delimiter=','):
    return genfromtxt(filePath, delimiter=delimiter) #return darray, read data from text file

def feature_normalize(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    return (dataset - mu)/sigma

def estimateGaussian(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.cov(dataset.T) #cov : covariance indicate whether two variables vary together (either same direction or opposite direction)
    return mu, sigma

def multivariateGaussian(dataset, mu, sigma): #multivariate gaussian is normal distribution to higher dimension
    p = multivariate_normal(mean=mu, cov=sigma)
    return p.pdf(dataset)

def selectThresholdByCV(probs, gt):
    best_epsilon = 0
    best_f1 = 0
    stepsize = (max(probs) - min(probs))/1000;
    epsilons = np.arange(min(probs), max(probs), stepsize) #arange return evenly spaced values in given range
    for epsilon in np.nditer(epsilons):
        predictions = (probs < epsilon)
        f = f1_score(gt, predictions, average = "binary")
        if f > best_f1:
            best_f1 = f
            best_epsilon = epsilon
    return best_f1, best_epsilon       

#-----------------
# read data 
#----------------- 
tr_data = read_dataset('C:\\Users\\a613274\\ML\\tr_server_data.csv')
tr_data
cv_data = read_dataset('C:\\Users\\a613274\\ML\\cv_server_data.csv')
cv_data
gt_data = read_dataset('C:\\Users\\a613274\\ML\\gt_server_data.csv')
gt_data

n_training_samples = tr_data.shape[0] #shape return tuple of narray dimension
n_training_samples
n_dim = tr_data.shape[1]
n_dim

plt.figure()
plt.xlabel("Latency (ms)")
plt.plot(tr_data[:,0], tr_data[:,1], "bx")
plt.show()
    

mu, sigma = estimateGaussian(tr_data)
mu
sigma

p = multivariateGaussian(tr_data, mu, sigma)
p

p_cv = multivariateGaussian(cv_data, mu, sigma)
p_cv
fscore, ep = selectThresholdByCV(p_cv, gt_data)
outliers = np.asarray(np.where(p < ep))

plt.figure()
plt.xlabel("Latency (ms)")
plt.ylabel("Throughput (mb/s)")
plt.plot(tr_data[:,0], tr_data[:,1], "bx") 
plt.plot(tr_data[outliers, 0], tr_data[outliers, 1], "ro")
plt.show()