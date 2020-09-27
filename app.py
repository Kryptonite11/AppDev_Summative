import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import base64
import datetime
import io
import dash_bootstrap_components as dbc

import numpy as np

import pickle

from sklearn.linear_model import LinearRegression # for linear regression modeling
from sklearn import preprocessing # for preprocessing like imputting missing values

from sklearn import metrics

from dash.dependencies import Input, Output, State
import dash_table



import requests
import json
import csv

from twilio.rest import Client


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)






# Style
# ------------------------------------------------------------------------------------------------------------------------------------------------------

colors = {
    'text': '#FFFFFF',
    'plot_color': '#000000',
    'paper_color': '#000000',
    'background_color': '#000000'

}

# ------------------------------------------------------------------------------------------------------------------------------------------------------


# Get Solar data
# ------------------------------------------------------------------------------------------------------------------------------------------------------

# Trenton, Australia
url = "https://api.openweathermap.org/data/2.5/onecall?lat=-19.461907&lon=142.110216&units=metric&exclude=current,minutely,hourly&appid=565b8d615f286ab8b932705dc2f6aa07"


response = requests.request("GET", url)
data = response.json()  # collecting data in JSON format

# Selecting daily data from JSON dataframe
dailyData = data['daily']

dailyDataDataframe = pd.DataFrame(dailyData)
print(dailyDataDataframe)


# Extracting temperature data

temp = dailyDataDataframe['temp']

day0 = temp.iloc[0]
day1 = temp.iloc[1]
day2 = temp.iloc[2]
day3 = temp.iloc[3]
day4 = temp.iloc[4]
day5 = temp.iloc[5]
day6 = temp.iloc[6]
day7 = temp.iloc[7]

temperatureDataDataframe = pd.DataFrame.from_dict([day0, day1, day2, day3, day4, day5, day6, day7])


fullWeatherForecastDataframe = pd.concat([dailyDataDataframe, temperatureDataDataframe], axis=1)

try:
  weatherForecastSolarDataframe = fullWeatherForecastDataframe[['max', 'min', 'clouds', 'rain']]
except:
  fullWeatherForecastDataframe['rain'] = 0
  weatherForecastSolarDataframe = fullWeatherForecastDataframe[['max', 'min', 'clouds', 'rain']]

weatherForecastSolarDataframe = fullWeatherForecastDataframe[['max', 'min', 'clouds', 'rain']]
weatherForecastSolarDataframe = weatherForecastSolarDataframe.fillna(0)
weatherForecastSolarDataframe["clouds"] = (weatherForecastSolarDataframe["clouds"].astype(float)/10)




X_testSolar = weatherForecastSolarDataframe 

# Load Model and apply pickled ML model
filename = 'solarMultipleLinearRegressionModel.sav'

loaded_model_solar = pickle.load(open(filename, 'rb'))

y_pred_solar = loaded_model_solar.predict(X_testSolar)
y_pred_solar = pd.DataFrame(y_pred_solar, columns = ['Power Predicted'])











# Get wind Data


# Germany
url = "https://api.openweathermap.org/data/2.5/onecall?lat=53.556563&lon=8.598084&units=metric&exclude=current,minutely,hourly&appid=565b8d615f286ab8b932705dc2f6aa07"

response = requests.request("GET", url)
data = response.json()  # collecting data in JSON format

# Selecting daily data from JSON dataframe
dailyData = data['daily']

dailyDataDataframe = pd.DataFrame(dailyData)
print(dailyDataDataframe)

weatherForecastWindDataframe = dailyDataDataframe[['wind_speed', 'wind_deg']]
weatherForecastWindDataframe = weatherForecastWindDataframe.fillna(0)


X_testWind = weatherForecastWindDataframe

# Load Model and apply pickled ML model
filename = 'windMultipleLinearRegressionModel.sav'

loaded_model = pickle.load(open(filename, 'rb'))

y_pred_wind = loaded_model.predict(X_testWind)
y_pred_wind = pd.DataFrame(y_pred_wind, columns = ['Power Predicted'])






# Weather API call 
# ------------------------------------------------------------------------------------------------------------------------------------------------------
#  OpenWeatherMap
#  https://openweathermap.org/api/one-call-api
#  apiKey = '565b8d615f286ab8b932705dc2f6aa07'


#  Solar farm
url = "https://api.openweathermap.org/data/2.5/onecall?lat=-19.461907&lon=142.110216&units=metric&exclude=current,minutely,hourly&appid=565b8d615f286ab8b932705dc2f6aa07"

response = requests.request("GET", url)
data = response.json()  # collecting data in JSON format

# Selecting daily data from JSON dataframe
dailyData = data['daily']

dailyDataDataframe = pd.DataFrame(dailyData)
print(dailyDataDataframe)

# Extracting temperature data

temp = dailyDataDataframe['temp']

day0 = temp.iloc[0]
day1 = temp.iloc[1]
day2 = temp.iloc[2]
day3 = temp.iloc[3]
day4 = temp.iloc[4]
day5 = temp.iloc[5]
day6 = temp.iloc[6]
day7 = temp.iloc[7]

temperatureDataDataframe = pd.DataFrame.from_dict([day0, day1, day2, day3, day4, day5, day6, day7])

fullWeatherForecastDataframe = pd.concat([dailyDataDataframe, temperatureDataDataframe], axis=1)

weatherForecastSolarDataframe = fullWeatherForecastDataframe[['max', 'min', 'clouds']]
weatherForecastSolarDataframe = weatherForecastSolarDataframe.fillna(0)
weatherForecastSolarDataframe["clouds"] = (weatherForecastSolarDataframe["clouds"].astype(float)/10)



#  Wind farm
url = "https://api.openweathermap.org/data/2.5/onecall?lat=53.556563&lon=8.598084&units=metric&exclude=current,minutely,hourly&appid=565b8d615f286ab8b932705dc2f6aa07"

response = requests.request("GET", url)
data = response.json()  # collecting data in JSON format

# Selecting daily data from JSON dataframe
dailyData = data['daily']

dailyDataDataframe = pd.DataFrame(dailyData)
print(dailyDataDataframe)


weatherForecastWindDataframe = dailyDataDataframe[['wind_speed', 'wind_deg']]
weatherForecastWindDataframe = weatherForecastWindDataframe.fillna(0)

# ------------------------------------------------------------------------------------------------------------------------------------------------------




# Data
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# Selecting daily data from JSON dataframe
dailyData = data['daily']

dailyDataDataframe = pd.DataFrame(dailyData)
dateTimeForecast = dailyDataDataframe[['dt']]

forecastDate = dateTimeForecast
forecastDate["dt"] = pd.to_datetime(forecastDate['dt'], unit='s')


forecastDate = pd.to_datetime(forecastDate['dt'], format="%Y/%m/%d")
forecastDate = forecastDate.to_frame()
forecastDate.rename(
    columns={'dt': 'Date'}, inplace=True)


forecastSolarPredictions = y_pred_solar
forecastWindPredictions = y_pred_wind


solarPredictedPower = pd.concat([forecastDate, forecastSolarPredictions], axis=1)
windPredictedPower = pd.concat([forecastDate, forecastWindPredictions], axis=1)


solarPredictedPower.rename(
    columns={'dt': 'Date', 'Power Predicted': 'Solar Power Predicted'}, inplace=True)
windPredictedPower.rename(
    columns={'dt': 'Date', 'Power Predicted': 'Wind Power Predicted'}, inplace=True)


solarPredictedPower['Date'] = solarPredictedPower['Date'].dt.date
windPredictedPower['Date'] = windPredictedPower['Date'].dt.date



global uploadedFileData
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# Figures
# ------------------------------------------------------------------------------------------------------------------------------------------------------

figSolar = px.line(solarPredictedPower, x="Date", y="Solar Power Predicted")
figWind = px.line(windPredictedPower, x="Date", y="Wind Power Predicted")

# ------------------------------------------------------------------------------------------------------------------------------------------------------



# Forecast Dataframes
# ------------------------------------------------------------------------------------------------------------------------------------------------------
forecastDataframeSolar = pd.concat([forecastDate, weatherForecastSolarDataframe ], axis =1)
forecastDataframeWind = pd.concat([forecastDate, weatherForecastWindDataframe ], axis =1)
# ------------------------------------------------------------------------------------------------------------------------------------------------------



# Twilio Credentials
# ------------------------------------------------------------------------------------------------------------------------------------------------------
account_sid = 'ACecab97f45f1c38d41805a74bd19ab341'
auth_token = '9d3626d4892f1308b995fe9aa037711c'
client = Client(account_sid, auth_token)
# ------------------------------------------------------------------------------------------------------------------------------------------------------











# Layout
# ------------------------------------------------------------------------------------------------------------------------------------------------------
app.layout = html.Div([


    html.H1(
        children='Power Production Dashboard',
        style={
            'textAlign': 'center'
        }
    ),

    html.Br(),

    html.H3(
        children="Weather forecast"
    ),    
    html.Div(
        children="Solar Farm - Trenton, Australia"
    ),

    dash_table.DataTable(
    id='solar-table',
    columns=[{"name": i, "id": i} for i in forecastDataframeSolar.columns],
    data=forecastDataframeSolar.to_dict('records'),
    ),


    html.Br(),
    
    html.Div(
        children="Wind Farm - Klushof, Germany"
    ),
    dash_table.DataTable(
    id='wind-table',
    columns=[{"name": i, "id": i} for i in forecastDataframeWind.columns],
    data=forecastDataframeWind.to_dict('records'),
    ),
    
    html.Br(),
    html.Br(),



    dcc.Graph
    (
        id="test-graph",
        figure={
            'data':
            [
                {
                    'x': solarPredictedPower['Date'],
                    'y':solarPredictedPower['Solar Power Predicted'],
                    'type':'line',  # bar
                    'name':'Solar Power Predicted'
                },
                {
                    'x': windPredictedPower['Date'],
                    'y':windPredictedPower['Wind Power Predicted'],
                    'type':'line',  # bar
                    'name':'Wind Power Predicted'
                }
            ],

            'layout':
            {
                'title': 'Estimated Power Production',
                'plot_bgcolor': colors['background_color'],
                'paper_bgcolor': colors['background_color'],
                'width': '200',
                'font':
                {
                    'color': colors['text']
                }
            }

        }
    ),



    html.Br(),
    html.Br(),







    # Current maintenance only works for upload file of today, and next 7 days


    dcc.Upload(id='maintenance-solar-upload', children=html.Div(['Solar Maintenance Upload ', html.A('Select Files')]),
               style={
        'width': '40%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'horizontal-align': 'left',
        'margin': '10px'
    },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    dcc.Upload(id='maintenance-wind-upload', children=html.Div(['Wind Maintenance Upload ', html.A('Select Files')]),
               style={
        'width': '40%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'horizontal-align': 'right',
        'margin': '10px'
    },
        # Allow multiple files to be uploaded
        multiple=True
    ),






    html.Table(id='table'),


    html.Div(id='intermediate-value', style={'display': 'none'}),


    # html.Button('testButton', id='test-button', n_clicks=0),

    html.Div(id='testSaveData'),


    # Hidden divs
    html.Div(id='hidden-dataframe-solar-maintenance',
             style={'display': 'none'}),
    html.Div(id='hidden-dataframe-wind-maintenance',
             style={'display': 'none'}),
    html.Div(id='hidden-alert-data',
             style={'display': 'none'}),
    html.Div(id='hidden-summary-data',
             style={'display': 'none'}),


    html.Br(),
    html.Button('Scale Production Data and Send Alerts',
                id='scale-production-by-maintenance'),
    html.Br(),


    html.Br(),

    
    html.Div(id='scaled-data'),



    html.Button('Send Alert',
                id='alert-data', style={'display': 'none'}),
    html.Button('Send Summary',
                id='summary-data', style={'display': 'none'}),

    html.Br(),


],


    style={
        'width': '75%',
        'display': 'inline-block',
        'vertical-align': 'middle',
        'horizontal-align': 'middle',
        'border': '1px solid black',
        'align-items': 'center',
        'padding': '20px'
}



)
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# Callbacks
# ------------------------------------------------------------------------------------------------------------------------------------------------------


# solar upload data file
@app.callback(Output('hidden-dataframe-solar-maintenance', 'children'),
              [Input('maintenance-solar-upload', 'contents')],
              [State('maintenance-solar-upload', 'filename'),
               State('maintenance-solar-upload', 'last_modified')])
def upload_solar_maintenance_file(list_of_contents, list_of_names, list_of_dates):
    df = None
    if list_of_contents is not None:
        df = parse_solar_dataframe(
            list_of_contents[0], list_of_names[0], list_of_dates[0])
        # print(df)
        return df.to_json()

# wind upload data file


@app.callback(Output('hidden-dataframe-wind-maintenance', 'children'),
              [Input('maintenance-wind-upload', 'contents')],
              [State('maintenance-wind-upload', 'filename'),
               State('maintenance-wind-upload', 'last_modified')])
def upload_wind_maintenance_file(list_of_contents, list_of_names, list_of_dates):
    df = None
    if list_of_contents is not None:
        df = parse_wind_dataframe(
            list_of_contents[0], list_of_names[0], list_of_dates[0])
        # print(df)
        return df.to_json()





@app.callback(Output('scaled-data', 'children'),
              [Input('hidden-dataframe-solar-maintenance', 'children')],
              [Input('hidden-dataframe-wind-maintenance', 'children')],
              [Input('scale-production-by-maintenance', 'n_clicks')])
def scale_production_data(solar_maintenance_data, wind_maintenance_data, value):
    # some expensive clean data step
    if value is not None:
        df_solar_maintenance = pd.read_json(solar_maintenance_data)
        df_wind_maintenance = pd.read_json(wind_maintenance_data)


        new_df = pd.DataFrame()
        new_df['Scaled Solar Predicted'] = df_solar_maintenance['Capacity Available as %'] * solarPredictedPower['Solar Power Predicted'] * (1/100)
        new_df['Scaled Wind Predicted'] = df_wind_maintenance['Capacity Available as %'] * windPredictedPower['Wind Power Predicted'] * (1/100)
        new_df['Total Power Production Predicted'] = new_df['Scaled Solar Predicted']  + new_df['Scaled Wind Predicted']


        return html.Div([

            dcc.Graph
            (
                id="abc-graph",
                figure={
                    'data':
                    [
                        {
                            'x': solarPredictedPower['Date'],
                            'y': new_df['Scaled Solar Predicted'],
                            'type':'line',  # bar
                            'name':'Solar Power Predicted Scaled'
                        },
                        {
                            'x': windPredictedPower['Date'],
                            'y': new_df['Scaled Wind Predicted'],
                            'type':'line',  # bar
                            'name':'Wind Power Predicted Scaled'
                        }
                    ],

                    'layout':
                    {
                        'title': 'Scaled Power Production',
                        'plot_bgcolor': colors['background_color'],
                        'paper_bgcolor': colors['background_color'],
                        'width': '200',
                        'font':
                        {
                            'color': colors['text']
                        }
                    }

                }
                
            ),

            dcc.Graph
            (
                id="total-graph",
                figure={
                    'data':
                    [
                        {
                            'x': solarPredictedPower['Date'],
                            'y': new_df['Total Power Production Predicted'],
                            'type':'line',  # bar
                            'name':'Solar Power Predicted Scaled'
                        }
                    ],

                    'layout':
                    {
                        'title': 'Total Power Production Predicted ',
                        'plot_bgcolor': colors['background_color'],
                        'paper_bgcolor': colors['background_color'],
                        'width': '200',
                        'font':
                        {
                            'color': colors['text']
                        }
                    }

                }
                
            ),

        ])







@app.callback(Output('hidden-alert-data', 'children'),
              [Input('hidden-dataframe-solar-maintenance', 'children')],
              [Input('hidden-dataframe-wind-maintenance', 'children')],
              [Input('scale-production-by-maintenance', 'n_clicks')])
def send_alert_data(solar_maintenance_data, wind_maintenance_data, value):
    # some expensive clean data step
    if value is not None:
        df_solar_maintenance = pd.read_json(solar_maintenance_data)
        df_wind_maintenance = pd.read_json(wind_maintenance_data)

        new_df = pd.DataFrame()
        new_df['Scaled Solar Predicted'] = df_solar_maintenance['Capacity Available as %'] * solarPredictedPower['Solar Power Predicted'] * (1/100)
        new_df['Scaled Wind Predicted'] = df_wind_maintenance['Capacity Available as %'] * windPredictedPower['Wind Power Predicted'] * (1/100)
        new_df['Total Power Production Predicted'] = new_df['Scaled Solar Predicted']  + new_df['Scaled Wind Predicted']



        Day0 = "" 
        Day1 = ""
        Day2 = ""
        Day3 = ""
        Day4 = ""
        Day5 = ""
        Day6 = ""
        Day7 = ""

        Day0Str = "" 
        Day1Str = ""
        Day2Str = ""
        Day3Str = ""
        Day4Str = ""
        Day5Str = ""
        Day6Str = ""
        Day7Str = ""

        
        day0Date = datetime.date.today()
        day1Date = day0Date + datetime.timedelta(days=1)
        day2Date = day1Date + datetime.timedelta(days=1)
        day3Date = day2Date + datetime.timedelta(days=1)
        day4Date = day3Date + datetime.timedelta(days=1)
        day5Date = day4Date + datetime.timedelta(days=1)
        day6Date = day5Date + datetime.timedelta(days=1)
        day7Date = day6Date + datetime.timedelta(days=1)




    

        if new_df['Total Power Production Predicted'].iloc[0] < 4:
            Day0 = new_df['Total Power Production Predicted'].iloc[0]
            Day0Str = day0Date

        if new_df['Total Power Production Predicted'].iloc[1] < 4:
            Day1 = new_df['Total Power Production Predicted'].iloc[1]
            Day1Str = day1Date

        if new_df['Total Power Production Predicted'].iloc[2] < 4:
            Day2 = new_df['Total Power Production Predicted'].iloc[2]
            Day2Str = day2Date

        if new_df['Total Power Production Predicted'].iloc[3] < 4:
            Day3 = new_df['Total Power Production Predicted'].iloc[3]
            Day3Str = day3Date

        if new_df['Total Power Production Predicted'].iloc[4] < 4:
            Day4 = new_df['Total Power Production Predicted'].iloc[4]
            Day4Str = day4Date

        if new_df['Total Power Production Predicted'].iloc[5] < 4:
            Day5 = new_df['Total Power Production Predicted'].iloc[5]
            Day5Str = day5Date

        if new_df['Total Power Production Predicted'].iloc[6] < 4:
            Day6 = new_df['Total Power Production Predicted'].iloc[6]
            Day6Str = day6Date

        if new_df['Total Power Production Predicted'].iloc[7] < 4:
            Day7 = new_df['Total Power Production Predicted'].iloc[7]
            Day7Str = day7Date
            
        


        message = "Alert! Days with < 4MW of power production combined: {Day0Str} {Day0} {Day1Str} {Day1} {Day2Str} {Day2} {Day3Str} {Day3} {Day4Str} {Day4} {Day5Str} {Day5} {Day6Str} {Day6} {Day7Str} {Day7}".format(
        Day0=Day0, Day1=Day1, Day2=Day2, Day3=Day3, Day4=Day4, Day5=Day5, Day6=Day6, Day7=Day7, Day0Str=Day0Str, Day1Str=Day1Str, Day2Str=Day2Str, Day3Str=Day3Str, Day4Str=Day4Str, Day5Str=Day5Str, Day6Str=Day6Str, Day7Str=Day7Str )
        
        messageSummary0 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day0Date, solar=new_df['Scaled Solar Predicted'].iloc[0], wind=new_df['Scaled Wind Predicted'].iloc[0], combined=new_df['Total Power Production Predicted'].iloc[0])        
        messageSummary1 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day1Date, solar=new_df['Scaled Solar Predicted'].iloc[1], wind=new_df['Scaled Wind Predicted'].iloc[1], combined=new_df['Total Power Production Predicted'].iloc[1])        
        messageSummary2 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day2Date, solar=new_df['Scaled Solar Predicted'].iloc[2], wind=new_df['Scaled Wind Predicted'].iloc[2], combined=new_df['Total Power Production Predicted'].iloc[2])        
        messageSummary3 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day3Date, solar=new_df['Scaled Solar Predicted'].iloc[3], wind=new_df['Scaled Wind Predicted'].iloc[3], combined=new_df['Total Power Production Predicted'].iloc[3])        
        messageSummary4 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day4Date, solar=new_df['Scaled Solar Predicted'].iloc[4], wind=new_df['Scaled Wind Predicted'].iloc[4], combined=new_df['Total Power Production Predicted'].iloc[4])        
        messageSummary5 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day5Date, solar=new_df['Scaled Solar Predicted'].iloc[5], wind=new_df['Scaled Wind Predicted'].iloc[5], combined=new_df['Total Power Production Predicted'].iloc[5])        
        messageSummary6 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day6Date, solar=new_df['Scaled Solar Predicted'].iloc[6], wind=new_df['Scaled Wind Predicted'].iloc[6], combined=new_df['Total Power Production Predicted'].iloc[6])        
        messageSummary7 = "Date {date}: Solar Power Scaled Prediction {solar} Wind Power Scaled Prediction {wind} Combined Predicted Power {combined}".format(
        date=day7Date, solar=new_df['Scaled Solar Predicted'].iloc[7], wind=new_df['Scaled Wind Predicted'].iloc[7], combined=new_df['Total Power Production Predicted'].iloc[7])


        message = " \n" +message + " \n" +messageSummary0 + " \n" +messageSummary1 + " \n" +messageSummary2 + " \n" +messageSummary3 + " \n" +messageSummary4 + " \n" +messageSummary5 + " \n" +messageSummary6 + " \n" +messageSummary7  

        print(message)

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to='whatsapp:+27814419374'
        )






# ------------------------------------------------------------------------------------------------------------------------------------------------------





# parse solar dataframe
def parse_solar_dataframe(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    # Get scaled solar predicted power
    # print(df)

    new_df = pd.DataFrame()
    new_df['Scaled Solar Predicted'] = df['Capacity Available as %'] * \
        solarPredictedPower['Solar Power Predicted']

    return df


# parse wind dataframe
def parse_wind_dataframe(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

    new_df = pd.DataFrame()
    new_df['Scaled Wind Predicted'] = df['Capacity Available as %'] * \
        windPredictedPower['Wind Power Predicted']

    return df


# Running the App
# ------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=4050)
# ------------------------------------------------------------------------------------------------------------------------------------------------------
