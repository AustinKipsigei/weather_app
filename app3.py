from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "60efbddb88dd2481343c67fc1140524c"  # replace with your real OpenWeatherMap key

@app.route('/', methods=['GET', 'POST'])
def index3():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data, error = get_weather_by_city(city)

    return render_template('index3.html', weather=weather_data, error=error)


@app.route('/weather')
def weather_by_coords():
    """Fetch weather using coordinates (lat, lon)."""
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Missing coordinates'}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

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
        return jsonify(weather_data)

    except requests.exceptions.RequestException:
        return jsonify({'error': 'Unable to fetch weather data'}), 500


def get_weather_by_city(city):
    """Fetch weather data for a given city name."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

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
