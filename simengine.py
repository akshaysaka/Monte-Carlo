import numpy as np
from presim import Inputs
from presim import generate_rnd

#Creating the proper Deposit and Withdrawals arrays
deposits = []
withdrawals = []

years = Inputs.Years[-1]
months = years*12


"""
An array to give 12 spaces between each withdrawal amount. Done to make the withdrawals annual. 
This is becasuse the simulations are monthly and the withdrawals are annual
This block of code prints a Deprecation warning becasue of the division performed in indexing
"""



def simulation(sim_ret,paths,steps):
	
	#Assigning aggregate withdrawal
	agg_withdrawal = Inputs.agg_withdrawal

	#performing simulations
	rcp = np.cumprod(sim_ret+1, axis = 1)
	agg_by_rcp = agg_withdrawal/rcp
	portfolio_values = rcp * (Inputs.Init_Value - np.cumsum(agg_by_rcp,axis = 1))

	#Discarding all the non-end of year values
	portfolio_values = portfolio_values[:,np.arange(0,portfolio_values.shape[-1],12)]
	
	return portfolio_values
	

# portfolio_values = simulation()
# print(portfolio_values)