from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "60efbddb88dd2481343c67fc1140524c"  # Replace with your real OpenWeatherMap key

@app.route('/', methods=['GET', 'POST'])
def index2():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')

        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if data.get('cod') != 200:
                    error = data.get('message', 'City not found.')
                else:
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

            except requests.exceptions.RequestException:
                error = "Network error. Please try again."

    return render_template('index2.html', weather=weather_data, error=error)


def get_background(weather_type):
    """Return background image filename based on weather."""
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
