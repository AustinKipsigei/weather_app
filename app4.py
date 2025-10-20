from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "60efbddb88dd2481343c67fc1140524c"  # Replace with your actual OpenWeatherMap key


@app.route('/', methods=['GET', 'POST'])
def index4():
    weather_data = None
    forecast_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data, error = get_weather_by_city(city)
            if weather_data:
                forecast_data = get_forecast_by_city(city)

    return render_template('index4.html', weather=weather_data, forecast=forecast_data, error=error)


@app.route('/weather')
def weather_by_coords():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing coordinates'}), 400

    try:
        # Current weather
        current_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        current_res = requests.get(current_url)
        current_res.raise_for_status()
        data = current_res.json()

        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'background': get_background(data['weather'][0]['main'].lower())
        }

        # 5-day forecast
        forecast_data = get_forecast_by_coords(lat, lon)

        return jsonify({'weather': weather_data, 'forecast': forecast_data})

    except requests.exceptions.RequestException:
        return jsonify({'error': 'Unable to fetch weather data'}), 500


def get_weather_by_city(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        if data.get('cod') != 200:
            return None, data.get('message', 'City not found.')

        main_weather = data['weather'][0]['main'].lower()
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'background': get_background(main_weather)
        }
        return weather_data, None
    except requests.exceptions.RequestException:
        return None, "Network error. Please try again."


def get_forecast_by_city(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return extract_daily_forecast(data)
    except:
        return None


def get_forecast_by_coords(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return extract_daily_forecast(data)
    except:
        return None


def extract_daily_forecast(data):
    """Convert 3-hourly forecast data into daily summaries."""
    daily = {}
    for item in data.get('list', []):
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        temp = item['main']['temp']
        icon = item['weather'][0]['icon']
        desc = item['weather'][0]['description']
        # Keep midday entries (12:00:00) or first seen per day
        if '12:00:00' in item['dt_txt'] or date not in daily:
            daily[date] = {
                'temp': round(temp, 1),
                'icon': icon,
                'desc': desc.capitalize()
            }
    # Return first 5 days only
    return list(daily.items())[:5]


def get_background(weather_type):
    if 'cloud' in weather_type:
        return 'cloudy.jpg'
    elif 'rain' in weather_type:
        return 'rainy.jpg'
    elif 'sun' in weather_type or 'clear' in weather_type:
        return 'sunny.jpg'
    elif 'snow' in weather_type:
        return 'snow.jpg'
    else:
        return 'default.jpg'


if __name__ == "__main__":
    app.run(debug=True)
