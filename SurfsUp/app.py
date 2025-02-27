# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base 
from collections import OrderedDict


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

# I coipied the codes for calculating the latest_date and previous_last_date from the analysis 
# notebook for easy access. 
# Starting from the most recent data point in the database. 
latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
# Calculate the date one year from the last date in data set.
previous_last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
# I also copied the code that identified the most active station: 
active_stations = (session.query(Measurement.station, func.count(Measurement.station))
                   .group_by(Measurement.station).order_by(func.count(Measurement.station).desc())).all()
most_active_station = active_stations[0][0]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# The first app is the landing page where the available routes are listed. 
@app.route("/")
def home():
    """List all the available routes."""
    return (
        f"Hawaii Climate API.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# The precipitation route is the second route. It returns a jsonified precepitation data for the last year in the database. 
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns the JSON representation of the query results from the precipitation analysis"""
    session = Session(engine)
    results = (session.query(Measurement.date, Measurement.prcp)
               .filter(Measurement.date >= previous_last_date)
               .order_by(Measurement.date).all())
    session.close()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

# The stations route lists all nine stations that are in the database. 
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    station_list = [station[0] for station in results]
    return jsonify(station_list)

# The tobs route retuns jsonified data for the most active station (USC00519281) for a year. 
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year for the most-active station for the previous year of data"""
    session = Session(engine)
    results = (session.query(Measurement.date, Measurement.tobs)
               .filter(Measurement.station == most_active_station)
               .filter(Measurement.date >= previous_last_date).all())
    session.close()
    temperature_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    return jsonify(temperature_data)

# The start route accepts the start date as a parameter from the URL. Dates are to be entered in YYYY-MM-DD format. 
@app.route("/api/v1.0/<start>")
def temp_stats_start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature starting from a specified start date to the end of the dataset"""
    session = Session(engine)
    results = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )
    session.close()

    if results[0][0] is None:
        return jsonify({"Date not found. Please enter a start date"}), 404
    temp_stats = {
        "start_date": start,
        "min_temp": results[0][0],
        "avg_temp": results[0][1],
        "max_temp": results[0][2], 
    }

    return jsonify(temp_stats)

# The start/end route accepts the start and end dates as parameters from the URL. Dates are to be entered in YYYY-MM-DD/YYYY-MM-DD format. 
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_range(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range."""
    session = Session(engine)
    results = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )
    session.close()

    if results[0][0] is None:
        return jsonify({"Date range not found. Please enter start and end date."}), 404
    
    temp_stats = OrderedDict([
        ("start_date", start),
        ("end_date", end),
        ("min_temp", results[0][0]),
        ("avg_temp", results[0][1]),
        ("max_temp", results[0][2]), 
    ])
    
    return jsonify(temp_stats)

# Run the Flask app

if __name__ == "__main__":
    app.run(debug=True)