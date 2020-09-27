
The project was initialized by the following process:

	Run:
	
	# first, we need to collect the historical data to generate ML models (simple regression models). The models are then saved using Pickle, for future use.
	- solarPowerPredictionModel.py		# creates pickle file solarMultipleLinearRegressionModel.sav
	- windPowerPredictionModel.py		# creates pickle file windMultipleLinearRegressionModel.sav
	
	
	
	# app.py loads the saved ML models using pickle, and applies the model to the input data, which is collected using a weather API (Open Weather Map)
	# The ML models are applied to the inputs from the APIs, which are then graphed using Dash
	
	# 2 buttons allow a user to upload CSV files for maintenance schedules, one for solar and one for wind (**currently, files need to include maintenance capacity for today, and the next 7 days)
	# The maintenance capacity then scales the estimated power predicted by the ML models, and graphs this data. The files in the project folder should be used for testing this functionality, where the capacities can be adjusted:
		# maintenance_solar.csv
		# maintenance_wind.csv
	
	# The user has the ability to send the summary and alerts to their cellphone number via Whatsapp (Whatsapp was only used to save costs using the Twilio trial. This can be easily changed to SMS messages)
		# The number can be changed in the app.py file, but the sandbox needs to be setup. Add the number +14155238886 to your phone contacts, then whatsapp the following message to this number:
		# "join ruler climb" without quotes
	# Alerts are sent for days in which there is a collective scaled Power Production estimated which is less than 4MW.
	# Pictures of the alerts and summary can be found in the Architecture folder
	- app.py
	
	
	
	
	
	
	




















