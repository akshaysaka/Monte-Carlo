# import simengine as se #Remove after finish
from presim import Inputs 
import scipy
from scipy import stats
import numpy as np
import pandas as pd



"""Takes a monthly rate. Converts it to a monthly rate such that if compounded, yields the yearly rate.
Discounts all columns using that rate. Discounts to time 0 (i.e. column 0 of x)
Changes the input array. 
"""

def discount(x, rate):

	#Preparing to get a row of discount rates
	disc_array = np.cumprod(np.ones((1,x.shape[-1]))*(rate+1))
	# print(disc_array)
	x = x/disc_array

	return x

"""
Getting the percentile values for every year.
Takes input from the inputs file and the result of the simulation (a numpy array).
Takes one argument which is the numpy array of the simulation result.
Returns a DataFrame of required percentiles. 
"""

def make_percentiles(x):

	#Creating Percentiles
	percentiles = np.array(Inputs.Percentiles)
	ptile_array = np.percentile(x,percentiles,axis = 0).T

	return ptile_array



"""
Obtain the probability of portfolio reaching the traget value in a list of years
"""
def target_probability(array,target,years):
	
	percentiles = []
	for year in years:
		percentiles.append(stats.percentileofscore(array[:,year-1],target))

	percentiles = np.array(percentiles)

	return (1-percentiles/100)
