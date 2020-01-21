{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "%matplotlib inline\n",
    "from matplotlib import style\n",
    "style.use('seaborn-dark')\n",
    "import matplotlib.pyplot as plt\n",
    "from sqlalchemy import desc\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "\n",
    "# Python SQL toolkit and Object Relational Mapper\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from flask import Flask,jsonify\n",
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")\n",
    "\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "# We can view all of the classes that automap found\n",
    "Base.classes.keys()\n",
    "\n",
    "\n",
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "\n",
    "# Create our session (link) from Python to the DB\n",
    "session = Session(engine)\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    \"\"\"List all available api routes.\"\"\"\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/<start><br/>\"\n",
    "        f\"/api/v1.0/<start>/<end>\"\n",
    "    )\n",
    "# Design a query to retrieve the last 12 months of precipitation data and plot the results\n",
    "# Calculate the date 1 year ago from the last data point in the database\n",
    "# Perform a query to retrieve the data and precipitation scores\n",
    "# Save the query results as a Pandas DataFrame and set the index to the date column\n",
    "# Sort the dataframe by date\n",
    "# Use Pandas Plotting with Matplotlib to plot the data\n",
    "\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "\n",
    "\n",
    "results = session.query(Measurement.prcp, Measurement.date).\\\n",
    " filter(Measurement.date < '2017-8-23').\\\n",
    " filter(Measurement.date > '2016-08-23').all()\n",
    "df = pd.DataFrame(results[:], columns=['prcp','date'])\n",
    "df.set_index('date', inplace=True)\n",
    "df.plot.bar(figsize=(12,8),title=\"precipation over dates\")\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "return jsonify(all_precipitation)\n",
    "\n",
    "# Use Pandas to calcualte the summary statistics for the precipitation data\n",
    "df.describe()\n",
    "# Design a query to show how many stations are available in this dataset?\n",
    "session.query(func.count(Station.station)).scalar()\n",
    "\n",
    "# What are the most active stations? (i.e. what stations have the most rows)?\n",
    "# List the stations and the counts in descending order.\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "sel = [Measurement.station,Measurement.tobs]\n",
    "station_tobs =session.query(*sel).order_by(Measurement.tobs.desc()).limit(10).all()\n",
    "print(station_tobs)\n",
    "\n",
    "return jsonify(all_stations)\n",
    "\n",
    "# Using the station id from the previous query, calculate the lowest temperature recorded, \n",
    "# highest temperature recorded, and average temperature of the most active station?\n",
    "session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).all()\n",
    "\n",
    "\n",
    "\n",
    "# Choose the station with the highest number of temperature observations.\n",
    "# Query the last 12 months of temperature observation data for this station and plot the results as a histogram\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "\n",
    "\n",
    "results=session.query(Measurement.station,Measurement.tobs, Measurement.date).\\\n",
    "     filter(Measurement.date < '2017-8-23').\\\n",
    "     filter(Measurement.date > '2016-08-23').\\\n",
    "     order_by(Measurement.tobs.desc()).\\\n",
    "     filter(Measurement.station == 'USC00519397').all()\n",
    "\n",
    "results_station= pd.DataFrame(results[:], columns=['Station','Tobs','Date'])\n",
    "results_station.head()\n",
    "\n",
    "return jsonify(all_tobs)\n",
    "\n",
    "results_station.plot.hist(figsize=(12,8),title=\"temperature observation data\")\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' \n",
    "# and return the minimum, average, and maximum temperatures for that range of dates\n",
    "@app.route(\"/api/v1.0/<start> \")\n",
    "def <start>():\n",
    "\n",
    "def calc_temps(start_date, end_date):\n",
    "   # \"\"\"TMIN, TAVG, and TMAX for a list of dates.\n",
    "    \n",
    "    #Args:\n",
    "        #start_date (string): A date string in the format %Y-%m-%d\n",
    "        #end_date (string): A date string in the format %Y-%m-%d\n",
    "        \n",
    "    #Returns:\n",
    "        #TMIN, TAVE, and TMAX\n",
    "    #\"\"\"\n",
    "    \n",
    "    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "\n",
    "# function usage example\n",
    "print(calc_temps('2012-02-28', '2012-03-05'))\n",
    "\n",
    "return jsonify(all_<start>)\n",
    "\n",
    "# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax \n",
    "# for your trip using the previous year's data for those same dates.\n",
    "@app.route(\"/api/v1.0/<start>/<end> \")\n",
    "def <start>/<end>():\n",
    "\n",
    "def calc_temps(start_date, end_date):\n",
    "    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\\\n",
    "        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()\n",
    "trip_temp = calc_temps('2017-08-07', '2017-08-23')\n",
    "trip_temp\n",
    "\n",
    "return jsonify(all_<start>/<end>)\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
