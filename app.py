from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace this with your actual API key
API_KEY = "60efbddb88dd2481343c67fc1140524c"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')

        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            print(url)
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon']
                }
            else:
                error = "City not found. Please try again."

    return render_template('index.html', weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
