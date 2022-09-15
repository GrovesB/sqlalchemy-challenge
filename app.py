import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
import pandas as pd
from sqlalchemy.engine.base import Engine

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine,reflect=True)

base.classes.keys()

# Save reference to the table
station = base.classes.station
measurement = base.classes.measurement


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and prcp
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(data))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    allstations = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(allstations))
    return jsonify(all_stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    top = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs), func.count(measurement.tobs)).\
    filter(measurement.station == 'USC00519281').all()
    session.close()

    all_tobs = list(np.ravel(top))
    
    return jsonify(all_tobs)


@app.route("/api/v1.0/temp/start")
def start():
    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(measurement.station, measurement.date, func.count(measurement.station), func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).all()
    
    session.close()

    start = []
    for station, date, count, min, max, avg in data:
        stationdata["Station"] = station
        stationdata["date"] = date
        stationdata["count"] = count(measurement.tabs)
        stationdata["min temp"] = min(measurement.tabs)
        stationdata["max temp"] = max(measurement.tabs)
        stationdata["average"] = avg(measurement.tabs)
        start.append(stationdata)
    return jsonify(start)


if __name__ == '__main__':
    app.run(debug=True)