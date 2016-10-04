import pandas as pd
import numpy as np

"""Importing the File and readying it for use."""
def read_data():
	df = pd.read_csv("Index_Returns.csv").drop(["SecId","Unnamed: 1"], axis = 1).T 
	df.columns = df.iloc[0]
	df = df.reset_index()
	df = df.drop(df.index[0])[:-1].dropna()
	df = df.reset_index()
	df =df.drop(["level_0","index"],axis = 1)
	df = df/100
	print(df[:5])

	return df
	

"""
Creating an Input object.
Used to call the weights, years, percent or dollar, tax rate etc.
Convert everything to a numpy array to speed up calcs. 
Only one instance of the class is required, hence called by the same name.
This was made because it's easier to access the input data as attributes of an object
"""

class Inputs:

	def __init__(self):
		self.Data = 		pd.read_csv("inputs.csv")
		self.Weights = 		np.array(self.Data.Weights.dropna())
		self.Tax =     		np.array(self.Data.Tax[0])
		self.Inflation = 	np.array(self.Data.Inflation[0])
		self.Withdrawals = 	np.array(self.Data.Cash_Withdrawal.fillna(0))
		self.Withdrawals = 	(self.Withdrawals*np.cumprod(np.ones((1,self.Withdrawals.shape[-1]))*(self.Inflation+1))).tolist()
		self.Deposits = 	np.array(self.Data.Cash_Deposits.fillna(0))
		self.Deposits = 	(self.Deposits*np.cumprod(np.ones((1,self.Deposits.shape[-1]))*(self.Inflation+1))).tolist()
		self.Securities = 	np.array(self.Data.Securities.dropna())
		self.Disc_Rate = 	np.array(self.Data.Discount_Rate[0])
		self.Percentiles = 	np.array(self.Data.Percentiles.dropna())
		self.Years = 		np.array(self.Data.Year.dropna())
		self.Months = 		int(self.Years[-1]*12)
		self.Init_Value = 	np.array(self.Data.Portfolio_Value.dropna())
		self.Expected_r = 	np.array(self.Data.Expected_yearly_return.dropna())
		self.Target = 		np.array(self.Data.Target_Value.dropna())
		self.Target_Years = np.array(self.Data.Target_Years.dropna())
		self.Historical = 	(self.Data.Years_Of_Hist_Data.dropna())

		

Inputs = Inputs() #Initializing Object

#Adding 0s to months unless it's the end of the year.
withdraw = []
deposit = []

for i in range(1,Inputs.Months+1): #Improve process to get rid of warning? Just add another indexing variable?
	if i%12 == 0: 
		j = i//12-1
		withdraw.append(Inputs.Withdrawals[j])
		deposit.append(Inputs.Deposits[j])
	else: 
		withdraw.append(0)
		deposit.append(0)

#converting to numpy arrays
Inputs.Withdrawals = np.array(withdraw)
Inputs.Deposits = np.array(deposit)
Inputs.agg_withdrawal = (Inputs.Withdrawals - Inputs.Deposits).reshape(1,Inputs.Months)
# print(Inputs.agg_withdrawal)

		#--Add percentage Withdrawals--


"""
Subsetting Data. 
Accepts a dataframe which is the universe of securities from which a few are selected for the simulation.
The securities to be selected are taken from the input file. (Specifically, the 'Inputs' object)
Creates the return stream of the portfolio using numpy's multiply.
"""
def prep_data(x):
	Historical = int(Inputs.Historical[0].tolist())
	data = x.filter(Inputs.Securities).dropna() #subsetting data for use in Simulations. 
	# print (len(data))
	# print(len(data[len(data)-(12*Historical):]))
	port_ret = np.array(np.sum(np.multiply(Inputs.Weights,data),axis = 1)) #Creating weighted returns.

	return port_ret



"""
Create random numbers using the inverse cdf method. Will shift the cdf according to the 
expexted return of the manager.
Takes prior returns to create the cdf
"""
def generate_rnd(returns,rows,cols):

	nobs = returns.size
	tax = Inputs.Tax

	#changing Expected return to monthly. Chaniging return to have mean equal to manager's expectation
	# print(Inputs.Expected_r)
	Inputs.Expected_r = np.exp(np.log(1+Inputs.Expected_r)/12)-1

	#Sorting the returns for the cdf, creating the cdf
	returns = np.sort(returns, kind = 'mergesort')
	cdf_values = np.arange(0,1,1./nobs)

	#Creating Antithetic Variance Reduced returns
	rnd = np.random.random((rows*cols//2)).reshape((rows,cols//2))
	mirror_rnd = 1-rnd
	rnd = np.append(rnd,mirror_rnd,axis = 1)

	#Interpolating from the CDF and finding the after tax returns
	sim_ret = np.interp(rnd,cdf_values,returns)
	sim_ret = sim_ret.flatten()
	sim_ret = np.random.choice(sim_ret,size = (rows,cols),replace = False)

	#Converting to after tax number
	sim_ret = (sim_ret>0)*(1-tax)*sim_ret+(sim_ret<=0)*sim_ret #After tax
	sim_ret = sim_ret - np.mean(sim_ret) 
	#Mean 0. Because the interpolation isn't capturing the mean perfectly. Maybe use Scipy's interpolation?

	# print(np.mean(returns)) 
	sim_ret = sim_ret + Inputs.Expected_r 

	# np.savetxt("sim Rets.csv",sim_ret,delimiter = ',')

	return sim_ret