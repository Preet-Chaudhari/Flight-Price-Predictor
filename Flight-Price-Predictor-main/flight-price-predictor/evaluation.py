import pickle
import pandas as pd
from keras import Sequential

NEW_MIN, NEW_MAX = 0, 1
airline_mapping = {'SpiceJet': 4, 'AirAsia': 0, 'Vistara': 5, 'Go_First': 2, 'Indigo': 3, 'Air_India': 1}
departure_time_mapping = {'Morning': 4, 'Early_Morning': 1, 'Evening': 2, 'Night': 5, 'Afternoon': 0, 'Late_Night': 3}
stops_mapping = {'zero': 2, 'one': 0, 'two_or_more': 1}
class_mapping = {'Economy': 1, 'Business': 0}


def load_model(model_name):
    return pickle.load(open(f"../model/{model_name}_model.pkl", 'rb'))


def get_min_max(attribute):
    dataset = pd.read_csv(r"../process_flight_dataset.csv")
    return dataset[attribute].min(), dataset[attribute].max()


def preprocess_data(airline, departure_time, stops, class_type, duration, days_left):
    encoded_airline = airline_mapping.get(airline)
    encoded_departure_time = departure_time_mapping.get(departure_time)
    encoded_class = class_mapping.get(class_type)
    encoded_stops = stops_mapping.get(stops.lower())

    # Scale 'duration' and 'days_left' as per model data
    duration_min, duration_max = get_min_max('duration')
    scaled_duration = (duration - duration_min) / (duration_max - duration_min) * (NEW_MAX - NEW_MIN) + NEW_MIN
    days_left_min, days_left_max = get_min_max('days_left')
    scaled_days_left = (days_left - days_left_min) / (days_left_max - days_left_min) * (NEW_MAX - NEW_MIN) + NEW_MIN

    return [encoded_airline, encoded_departure_time, encoded_stops, encoded_class, scaled_duration, scaled_days_left]


def predict(model_name, airline, departure_time, stops, class_type, duration, days_left):
    m = load_model(model_name)
    data = preprocess_data(airline, departure_time, stops, class_type, duration, days_left)
    prediction = m.predict([data])[0].round(2)
    price_min, price_max = get_min_max('price')
    return round(((prediction - NEW_MIN) * (price_max - price_min) / (NEW_MAX - NEW_MIN) + price_min), 2)


if __name__ == '__main__':
    # airline, departure, stops, class, duration, days_left
    predicted_price = predict('xgb', 'SpiceJet', 'Evening', 'zero', 'Economy', 2, 1)
    print("Predicted price: ", predicted_price)
