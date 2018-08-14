
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib
matplotlib.use('nbagg')
from matplotlib import style
#style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import matplotlib.dates as dates


# In[2]:


import numpy as np
import pandas as pd
import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[3]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, func, inspect
import numpy as np
import pandas as pd
from flask import Flask, jsonify

from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Index
from sqlalchemy import MetaData
from sqlalchemy import Table
import csv


# In[4]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[5]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[6]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[7]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[8]:


# Create our session (link) from Python to the DB
session = Session(engine)

inspector  = inspect(engine) 
inspector.get_table_names()


# In[9]:


columns = inspector.get_columns('measurement')

for c in columns:
    print(c['name'], c["type"])


# In[10]:


columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])


# In[11]:


engine.execute('SELECT * FROM measurement LIMIT 5').fetchall()


# In[12]:


engine.execute('SELECT * FROM station LIMIT 5').fetchall()


# In[13]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results

# Calculate the date 1 year ago from today

# Perform a query to retrieve the data and precipitation scores

# Save the query results as a Pandas DataFrame and set the index to the date column

# Sort the dataframe by date

# Use Pandas Plotting with Matplotlib to plot the data

# Rotate the xticks for the dates


# In[14]:


prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
prcp_results


# In[15]:


date = [prcp_results[0] for prcp_result in prcp_results[0:]]
prcp = [prcp_results[1] for prcp_result in prcp_results[0:]]
prcp_df= pd.DataFrame(prcp_results[0:], columns=['date', 'prcp'] )



prcp_df["date"] = pd.to_datetime(prcp_df["date"])

prcp_df.set_index('date', inplace=True, )
prcp_df.head(10)


# In[16]:


# Use Pandas to calcualte the summary statistics for the precipitation data
prcp_df.describe()


# In[39]:


years = dates.YearLocator()   # every year
months = dates.MonthLocator()  # every month
yearsFmt = dates.DateFormatter('%b-%Y')
prcp_df.plot()
#fig, ax = plt.subplots()

# format the ticks
#ax.xaxis.set_major_locator(months)
#ax.xaxis.set_major_formatter(yearsFmt)
#ax.xaxis.set_minor_locator(months)
plt.title('Hawaii Precipitation 12 months')
plt.xlabel('Date')
plt.ylabel('Precipitation')
plt.tight_layout()
plt.show()
fig.savefig('Hawaii_Precip_Last12months.png', dpi=fig.dpi)


# In[40]:


# How many stations are available in this dataset?

total_stations  = session.query(Measurement.station).distinct(Measurement.station).count()
print("Total Stations: "+ str(total_stations))


# In[41]:


# What are the most active stations?
# List the stations and the counts in descending order.
Most_active_stations = session.query(Measurement.station, func.count(Measurement.prcp)).                                     group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).all()
Most_active_stations


# In[42]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
lowest = session.query(Measurement.station, func.min(Measurement.prcp)).                    group_by(Measurement.station).filter(Measurement.station == 'USC00519281').first()

highest = session.query(Measurement.station, func.max(Measurement.prcp)).                    group_by(Measurement.station).filter(Measurement.station == 'USC00519281').first()

average = session.query(Measurement.station, func.avg(Measurement.prcp)).                    group_by(Measurement.station).filter(Measurement.station == 'USC00519281').first()
print ("lowest: ",lowest, "  Highest:",highest, "   Average: ", average)


# In[43]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

#that station is USC00519281
Most_active_stations = session.query(Measurement.station).                                group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).limit(1).scalar()

print ( "Most Active Station is  " + str(Most_active_stations))

Most_active_results = session.query(Measurement.station, Measurement.tobs).                                   filter(Measurement.date.between('2016-08-23', '2017-08-23')).                                   filter(Measurement.station == Most_active_stations).all()
Most_active_results


# In[44]:


Most_active_temp = [result[1] for result in Most_active_results[0:]]

fig, ax = plt.subplots()
plt.hist(Most_active_temp, bins = 12, align='mid', label="tobs", alpha=0.75, normed=1,color="b")
plt.title('Last Year Temperature at Station USC00519281')
plt.xlabel('Temperature')
plt.ylabel("Frequency")
plt.axis([55, 85, 0, 0.12])
plt.title('Histogram of Temperature')
fig.tight_layout()
plt.show()
fig.savefig('Histogram of Temperature.png', dpi=fig.dpi)


# In[45]:


# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
Temp=[]
def calc_temps(start_date, end_date):
    results=session.query(func.max(Measurement.tobs).label("max_tobs"),                           func.min(Measurement.tobs).label("min_tobs"),                          func.avg(Measurement.tobs).label("avg_tobs")).                          filter(Measurement.date.between(start_date , end_date))  
    res = results.one()
    res
    TMAX = res.max_tobs
    TMIN= res.min_tobs
    TAVG= res.avg_tobs
    #Temp = []
    Temp.append(TMAX)
    Temp.append(TMIN)
    Temp.append(TAVG)

    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    


# In[46]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.
print("min   avg    max ==>", calc_temps('2016-08-23', '2017-08-023'))


# In[47]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)
TAVG=Temp[2]
TMIN=Temp[1]
TMAX=Temp[0]
fig = plt.figure()
plt.bar( 1,TAVG, color = 'blue', yerr = TMAX-TMIN, align='center')
plt.xlim(-0.2, 2.2)
plt.ylim([0, 110])
plt.axes().get_xaxis().set_visible(False)
plt.title('Trip Avg Temp')
plt.ylabel('Temp (F)')
plt.tight_layout()
plt.show()
fig.savefig('Trip Avg Temp.png', dpi=fig.dpi)


# In[49]:


# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

#zZZZZZZZZZZZ

rainfall = []
rainfall = session.query(Measurement.station, func.count(Measurement.prcp)).                   group_by(Measurement.station).filter(Measurement.date.between('2016-08-23', '2017-08-23')).order_by(func.count(Measurement.prcp).desc()).all()
rainfall
  
    


# In[65]:


rainfall3 = []
rainfall3 =     session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).            order_by(Station.station).            all()

rainfall3


# In[74]:




killingme = session.query(Station.station, Station.name, Station.latitude,Station.longitude, Station.elevation, func.sum(Measurement.prcp)).    filter(Measurement.date.between('2016-08-23', '2017-08-23'))    .group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()

killingme


# ## Optional Challenge Assignment

# In[ ]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")


# In[ ]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# In[ ]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


# In[ ]:


# Plot the daily normals as an area plot with `stacked=False`

