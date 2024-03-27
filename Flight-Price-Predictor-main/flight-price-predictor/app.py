from flask import Flask, request
from flask import render_template
from evaluation import *

app = Flask(__name__)
BEST_MODEL = 'xgb'


@app.get('/')
def index():  # put application's code here
    return render_template('index.html', airlines=airline_mapping, departure_times=departure_time_mapping,
                           stops=stops_mapping, cabin_classes=class_mapping)


@app.get('/predict')
def predict_flight_price():
    airline = request.args.get('airline')
    departure_time = request.args.get('departure_time')
    stops = request.args.get('stops')
    cabin_classes = request.args.get('cabin_classes')
    duration = int(request.args.get('duration'))
    days_left = int(request.args.get('days_left'))
    return {"prediction": predict(BEST_MODEL, airline, departure_time, stops, cabin_classes, duration, days_left)}


if __name__ == '__main__':
    app.run()
