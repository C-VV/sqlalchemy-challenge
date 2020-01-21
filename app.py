#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('seaborn-dark')
import matplotlib.pyplot as plt
from sqlalchemy import desc
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Calculate the date 1 year ago from the last data point in the database
# Perform a query to retrieve the data and precipitation scores
# Save the query results as a Pandas DataFrame and set the index to the date column
# Sort the dataframe by date
# Use Pandas Plotting with Matplotlib to plot the data

@app.route("/api/v1.0/precipitation")
def precipitation():


results = session.query(Measurement.prcp, Measurement.date). filter(Measurement.date < '2017-8-23'). filter(Measurement.date > '2016-08-23').all()
df = pd.DataFrame(results[:], columns=['prcp','date'])
df.set_index('date', inplace=True)
df.plot.bar(figsize=(12,8),title="precipation over dates")
plt.tight_layout()
plt.show()

return jsonify(all_precipitation)

# Use Pandas to calcualte the summary statistics for the precipitation data
df.describe()
# Design a query to show how many stations are available in this dataset?
session.query(func.count(Station.station)).scalar()

# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
@app.route("/api/v1.0/stations")
def stations():
sel = [Measurement.station,Measurement.tobs]
station_tobs =session.query(*sel).order_by(Measurement.tobs.desc()).limit(10).all()
print(station_tobs)

return jsonify(all_stations)

# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).all()



# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
@app.route("/api/v1.0/tobs")
def tobs():


results=session.query(Measurement.station,Measurement.tobs, Measurement.date).     filter(Measurement.date < '2017-8-23').     filter(Measurement.date > '2016-08-23').     order_by(Measurement.tobs.desc()).     filter(Measurement.station == 'USC00519397').all()

results_station= pd.DataFrame(results[:], columns=['Station','Tobs','Date'])
results_station.head()

return jsonify(all_tobs)

results_station.plot.hist(figsize=(12,8),title="temperature observation data")
plt.tight_layout()
plt.show()

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
@app.route("/api/v1.0/<start> ")
def <start>():

def calc_temps(start_date, end_date):
   # """TMIN, TAVG, and TMAX for a list of dates.
    
    #Args:
        #start_date (string): A date string in the format %Y-%m-%d
        #end_date (string): A date string in the format %Y-%m-%d
        
    #Returns:
        #TMIN, TAVE, and TMAX
    #"""
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))

return jsonify(all_<start>)

# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
@app.route("/api/v1.0/<start>/<end> ")
def <start>/<end>():

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
trip_temp = calc_temps('2017-08-07', '2017-08-23')
trip_temp

return jsonify(all_<start>/<end>)


if __name__ == "__main__":
    app.run(debug=True)


