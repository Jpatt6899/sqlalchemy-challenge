import numpy as np
import datetime as dt

import sqlalchemy
import pandas as pd 

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def welcome():

    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    
    session = Session(engine)
     
    
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

    session.close()
    
@app.route("/api/v1.0/stations")
def stations():
   
    
    session = Session(engine)
    station_list = session.query(Station.station).all()
    station_f = list(np.ravel(station_list)) 
    return jsonify(station_f)
    
    
    session.close()

    
    
    
@app.route("/api/v1.0/tobs")
def temp_monthly():
    
    session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    weather_year_top = session.query(Measurement.tobs, Measurement.station, Measurement.date).\
        filter(or_(Measurement.date > prev_year, Measurement.station == 'USC00519281')).all()
    w_t = list(np.ravel(weather_year_top)) 
    return jsonify(w_t)

    session.close()
  


@app.route("/api/v1.0/temp/<start>/<end>")


def stats_end(start=None, end=None):

    session = Session(engine)
    start_date = dt.date(2014, 8, 23)
    end_date = dt.date(2015, 8, 23)
 
       
    max_temp_end = session.query(func.max(Measurement.tobs)).\
        filter(and_(Measurement.date >= start_date, Measurement.date < end_date)).all()  
    
    min_temp_end = session.query(func.min(Measurement.tobs)).\
        filter(and_(Measurement.date >= start_date, Measurement.date < end_date)).all() 
    
    avg_temp_end = session.query(func.avg(Measurement.tobs)).\
        filter(and_(Measurement.date >= start_date, Measurement.date < end_date)).all()
     
    dict_temp = {
      'Max' : max_temp_end,
      'Min' : min_temp_end,
      'Avg' : avg_temp_end
      
    }
    return jsonify(dict_temp)
    
    session.close()

@app.route("/api/v1.0/temp/<start>")

def stats(start=None, end=None):
    
    session = Session(engine)
    start_date = dt.date(2014, 8, 23)
    

    max_temp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all() 
    
    min_temp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all() 
    
    avg_temp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all() 
     
    dict_temp = {
      'Max' : max_temp,
      'Min' : min_temp,
      'Avg' : avg_temp
      
    }
    return jsonify(dict_temp)
    
    session.close()
    

    
    

    
    



if __name__ == '__main__':
    app.run()
    
    
    
    
    
