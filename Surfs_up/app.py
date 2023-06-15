# Import the dependencies.
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta

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
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/measurements
        /api/stations
        /api/precipitation
        /api/tobs
        /api/start_route
        /api/start_end_route
        ''')

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

    # Return the stations as JSON
    return jsonify(stations)

# Define the precipitation route
@app.route('/api/precipitation')
def get_precipitation():
    # Calculate the date one year ago from today
    one_year_ago = datetime(2017, 8, 23) - timedelta(days=365)

    # Query the measurement table for precipitation data in the last year
    results = session.query(Measurement.date, Measurement.prcp) \
                     .filter(Measurement.date >= one_year_ago) \
                     .order_by(Measurement.date) \
                     .all()

    # Create a dictionary with date as the key and precipitation as the value
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp

    # Return the precipitation data as JSON
    return jsonify(precipitation_data)

# Define the tobs route
@app.route('/api/tobs')
def get_tobs():
    # Calculate the date one year ago from today
    one_year_ago = datetime(2017, 8, 23) - timedelta(days=365)

    # Query the most active station
    most_active_station = session.query(Measurement.station) \
                                 .group_by(Measurement.station) \
                                 .order_by(func.count().desc()) \
                                 .first()

    # Query the measurement table for temperature data from the most active station in the last year
    results = session.query(Measurement.date, Measurement.tobs) \
                     .filter(Measurement.station == most_active_station[0]) \
                     .filter(Measurement.date >= one_year_ago) \
                     .order_by(Measurement.date) \
                     .all()

    # Create a list of dictionaries with date as the key and temperature as the value
    tobs_data = []
    for date, tobs in results:
        tobs_data.append({'date': date, 'temperature': tobs})

    # Return the tobs data as JSON
    return jsonify(tobs_data)

# Define the start route
@app.route('/api/start_route')
def get_temperatures_start():
    # Get the start date parameter from the URL
    start_date = request.args.get('start')

    # Convert the start date to a datetime object
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Query the measurement table for min, max, and average temperatures from the start date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
                     .filter(Measurement.date >= start_date) \
                     .all()

    # Extract the results
    min_temp, max_temp, avg_temp = results[0]

    # Create a dictionary with the temperature data
    temperature_data = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': 'latest',
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'avg_temperature': avg_temp
    }

    # Return the temperature data as JSON
    return jsonify(temperature_data)

# Define the start/end route
@app.route('/api/start_end_route')
def get_temperatures_start_end():
    # Get the start and end dates parameters from the URL
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Convert the start and end dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Query the measurement table for min, max, and average temperatures from the start date to the end date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
                     .filter(Measurement.date >= start_date, Measurement.date <= end_date) \
                     .all()

    # Extract the results
    min_temp, max_temp, avg_temp = results[0]

    # Create a dictionary with the temperature data
    temperature_data = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'min_temperature': min_temp,
        'max_temperature': max_temp,
        'avg_temperature': avg_temp
    }

    # Return the temperature data as JSON
    return jsonify(temperature_data)


# Run Flask app
if __name__ == '__main__':
    app.run()
