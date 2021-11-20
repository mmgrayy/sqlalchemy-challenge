import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import time

#initialize database connection 
engine = create_engine("sqlite:////Users/meredithgray/Desktop/sqlalchemy-challenge/Resources/hawaii.sqlite ")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)
# NOW the Flask Setup
app = Flask(__name__)
#Homepage
@app.route("/")
def Home():
    print("This is my homepage")
    return "Welcome to the Climate Analysis API for the great state of Hawaii! <br/>  <br/> Here is a list of all available API routes: <br/> <br/> /api/v1.0/precipitation <br/> /api/v1.0/stations <br/> /api/v1.0/tobs <br/> /api/v1.0/<start> <br/> When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date <br/> /api/v1.0/<start>/<end><br/> When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive <br/> Please copy and paste to the end of the address to view."

#Participation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-24').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()
    prcp_dict= {date:prcp for date,prcp in results}
    session.commit()
    time.sleep(2)

    # Convert list of tuples into normal list
    return jsonify(prcp_dict)
    

@app.route("/api/v1.0/stations")
def stations():
    print("The Station List.")
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    session.commit()
    time.sleep(2)

    # Convert list of tuples into normal list
    return jsonify(stations.to_dict())

@app.route("/api/v1.0/tobs")
def temp_monthly():
    print("TOBS")
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-24').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()
    tobs_dict= {date:tobs for date,tobs in results}
    session.commit()
    time.sleep(2)

    # Convert list of tuples into normal list/Users/meredithgray/Desktop/sqlalchemy-challenge/practicing.py
    return jsonify(tobs_dict)


@app.route("/api/v1.0/<date>")
def startDateOnly(date):
    print("Start")
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date).all()
    session.commit()
    time.sleep(2)

    # Convert list of tuples into normal list
    return jsonify(day_temp_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.commit()
    time.sleep(2)

    # Convert list of tuples into normal list
    return jsonify(multi_day_temp_results)
    
if __name__ == '__main__':
    app.run(debug=True)
