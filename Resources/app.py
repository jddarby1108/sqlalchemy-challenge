# Docs on session basics
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html

import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/stations"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    """Return a list of all precipitation data"""

    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    
    print(all_names)
    return jsonify(all_names)

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    # all_prcp = []
    # for row in results:
    #     prcp_dict = {}
    #     row.date = row.prcp
    #     prcp_dict = {"date", "prcp"}
    #     all_prcp.append(prcp_dict)
    # # print(all_prcp)
    # return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all precipitation data"""

    # Query all passengers
    session = Session(engine)
    results = session.query(Station.name).all()
    
    # close the session to end the communication with the database
    session.close()

    all_stations = list(np.ravel(results))
    
    print(all_stations)
    return jsonify(all_stations)

    
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs data"""

    # Query all most active station
    session = Session(engine)
    results = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs)).all()[-1]
    
    # close the session to end the communication with the database
    session.close()

    all_tobs = list(np.ravel(results))
    
    print(all_tobs)
    return jsonify(all_tobs)

# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""

#     # Open a communication session with the database
#     session = Session(engine)

#     # Query all passengers
#     results = session.query(Passenger).all()

#     # close the session to end the communication with the database
#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
