# Monte-Carlo
Performs Monte Carlo with returns based on the CDF of the portfolio being modeled

**************************************************
Readme for the Monte carlo Software
**************************************************
-> There are three main files the user directly uses: Monte-Carlo.py, inputs.csv, Index_Returns.csv

-> Don't change the top row of the inputs.csv file.

-> Save the inputs.csv file before running the program.

-> Make sure the Final Outputs.csv file is closed.

-> Make sure all three files are in the same folder.

-> Don't change the names of the three files.

-> All percentage numbers are to be between 0 and 1.

-> Don't change the format type of the cells in the csv files.

***************************************************
Setting up inputs
***************************************************
-> PORTFOLIO VALUE: 	The starting value. Insert dollar amount. Only one Value.

-> SECURITIES: 		Takes the names of the securities from the Index_Returns.csv file. 
			Take multiple names.
			Names have to match exactly from the Index_Returns.csv file.

-> WEIGHTS:		Weights of the securities in the portfolio. 
			Takes values exactly in line with the securities.
			Values need to be between 0 and 1.
			No check to see if sum > 1. If it is, it will assume a levered position.

-> YEAR:		Takes the number of years of simulation. 
			Add every year starting from 1 to last year.

-> CASH_WITHDRAWAL:	Assumes as many cash withdrawals as years. 
			Enter dollar value.
			If empty, takes 0.
			Vaues are compounded at inflation rate automatically in the program.
			Withdrawals are before tax.
			All transactions assumed at end of year.

-> CASH_DEPOSITS:	Same as withdrawals. 

-> TAX:			Enter one number between 0 and 1. Applied to the portfolio value. Not to the Cash Withdrawals. 

-> DISCOUNT_RATE:	Enter one number between 0 and 1. 
			Applied to the portfolio values.

-> INFLATION_RATE:	Enter one number between 0 and 1.
			Applied to the cash withdrawals and deposits.

-> PERCENTILES: 	Takes multiple values. 
			Values between 0 and 99. 

-> EXPECTED_YEARLY_RET:	Takes one value between 0 and 1. (Technically, >1 would mean more than 100% return)

-> TARGET_VALUE:	Take one value. 
			Checks the chances of achieving that value in the target years.

-> TARGET_YEARS:	Takes multiple values.
			Checks the probability of being higher than the traget value during each of those years.

-> YEARS_OF_HIST_DATA:	No. of years of historical data to take. Current max = 13 years.


**************************************************
Adding returns to Index_Returns.csv
**************************************************
-> Don't add returns after the last column. The last column has the index sarting date. Add returns before that.

-> Don't delete any of the non-returns columns. 

-> You can add other indexes below the existing list.

-> Numbers are percentages*100. Enter the values for a new index in the same way.

-> Save your changes!
