# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


# Create our session (link) from Python to the DB
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    # Query for last 12 months of data
    last_date = '2017-08-23'
    start_date = '2016-08-23'
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date <= last_date).filter(measurement.date >= start_date).all()
    session.close()
    
    past_year = []
    for date, prcp in results:
        past_dict = {}
        past_dict['Date'] = date
        past_dict['precipitation'] = prcp
        past_year.append(past_dict)
    return jsonify(past_year)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    
    all_station = list(np.ravel(results))
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = '2017-08-23'
    start_date = '2016-08-23'

    results = session.query(measurement.tobs, measurement.date).filter(measurement.date <= last_date).filter(measurement.date >= start_date).filter(measurement.station == 'USC00519281').all()
    session.close()
    
    past_year = []
    for tobs, date in results:
        past_dict = {}
        past_dict['Temp'] = tobs
        past_dict['Date'] = date
        past_year.append(past_dict)
    return jsonify(past_year)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['min'] = min
        temp_dict['avg'] = avg
        temp_dict['max'] = max
        temp_list.append(temp_dict)
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date <= end).filter(measurement.date >= start).all()
    session.close()
    temp_list = []
    for min, avg, max in results:
        temp_dict = {}
        temp_dict['min'] = min
        temp_dict['avg'] = avg
        temp_dict['max'] = max
        temp_list.append(temp_dict)
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)

        