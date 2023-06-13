# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# Set up the database connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

#################################################
# Flask Setup
#################################################
# Instance of Flask app
app= Flask(__name__)


#################################################
# Flask Routes
#################################################

# Define route to retrieve measurements 
@app.route('/api/measurements')
def get_measurements():
    # Query the measurement table
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert the query results to a list of dictionaries
    measurements = []
    for date, prcp in results:
        measurement = {'date': date, 'prcp': prcp}
        measurements.append(measurement)

    # Return the measurements as JSON
    return jsonify(measurements)

# Define a route to retrieve stations
@app.route('/api/stations')
def get_stations():
    # Query the station table
    results = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations = []
    for station, name in results:
        station_data = {'station': station, 'name': name}
        stations.append(station_data)

# Run Flask app
if __name__ == '__main__':
    app.run()
