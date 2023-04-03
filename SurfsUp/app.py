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
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/") #establishes the home route for the server
def home():
    
    print("List all the available routes.")
    return (
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    prcp_scores = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-24").all()
    session.close()
# Convert prcp_scores query results to a dictionary.
    prcp_data = []
    for date,prcp in prcp_scores:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    mostActive_stations = session.query(measurement.station, func.count(measurement.station)).\
    group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    mostActive_stations
    session.close()
    stations_list = list(np.ravel(mostActive_stations))
    return jsonify(stations_list)


# Return a JSON list of tobs for the previous year.


if __name__ == "__main__":
    app.run(debug=True)
