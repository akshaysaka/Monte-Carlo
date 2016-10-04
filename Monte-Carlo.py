print('Importing dependencies...\n\n\n')
import numpy as np
import pandas as pd
import simengine as se
import postsim as postsim
from presim import Inputs
from presim import prep_data
from presim import read_data
from presim import generate_rnd


if __name__ == "__main__":

	print("Reading inputs & past data...\n\n\n")
	#Reading and preparing data
	universe = read_data()
	returns = prep_data(universe)
	months = Inputs.Months

	print("Preparing some stuff for the simulation...\n\n\n")
	#setting number of paths and number of steps in each path
	nPaths = 50000
	nSteps = months

	print("Generating random returns...\n\n\n")
	#Generate returns based on past returns
	sim_ret = generate_rnd(returns,nPaths,nSteps)
	# print(np.mean(sim_ret))

	print("Performing simulations...\n\n\n")
	#Performing Simulations
	simulation = se.simulation(sim_ret,nPaths,nSteps)
	print("Simulations complete. \n\n\n")
	
	print("Discounting results...\n\n\n")
	#Discounting the result of the simulation
	simulation = postsim.discount(simulation,Inputs.Disc_Rate)

	print("Calculating percentiles...\n\n\n")
	#Making the twenty percentiles for every year of the simulation
	percentiles = postsim.make_percentiles(simulation)
	percentiles = np.insert(percentiles,0,Inputs.Init_Value,axis = 0 )

	print("Finding the probabilities of reaching target...\n\n\n")
	#Finding the probability of the target in that year
	probabilities = postsim.target_probability(simulation,Inputs.Target,Inputs.Target_Years)
	
	print("Aggregating results...\n\n\n")
	#Adding the results to a dataframe
	result = pd.DataFrame(percentiles)
	result = pd.concat([result,pd.DataFrame(Inputs.Target_Years),pd.DataFrame(probabilities)],axis = 1)

	columns=[]
	for i in Inputs.Percentiles:
		columns.append("%dth percentile" %i)

	columns.append("Target Years")
	columns.append("Probabilities of achieving %d" %Inputs.Target)

	result.columns = columns
	# result.index = np.arange(1,Inputs.Years[-1]+2)
	result.index.names = ["Years"]

	print("Writing to csv...")
	#Results to csv
	result.to_csv("Final Output.csv")

	exit = input("\n\n\n\nIgnore the Warning.\nDone. Press Enter to exit.")
