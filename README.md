# 🌦️ Live Weather App  

A sleek, responsive **Flask-powered Weather Application** that fetches **real-time weather data** using the [OpenWeatherMap API](https://openweathermap.org/).  
It includes **interactive maps**, **unit toggling (°C / °F)**, **recent search history**, and **auto-detection of user location** — all wrapped in a modern, clean UI.  

---

## 🚀 Features  

✅ **Live Weather Data** – Displays current temperature, conditions, humidity, wind speed, and “feels like” info.  
✅ **5-Day Forecast** – Fetches extended forecasts for any searched location.  
✅ **Interactive Map** – Built with [Leaflet.js](https://leafletjs.com/); click anywhere on the map to get weather updates for that spot.  
✅ **Auto Location Detection** – Automatically shows your weather when you open the app (via browser geolocation).  
✅ **Search History** – Keeps track of your recent city searches for quick access.  
✅ **Temperature Unit Toggle** – Seamlessly switch between **Celsius (°C)** and **Fahrenheit (°F)**.  
✅ **Responsive UI** – Built with Bootstrap for full mobile and desktop support.  

---

## 🛠️ Technologies Used  

| Category | Tools / Frameworks |
|-----------|--------------------|
| **Backend** | [Flask](https://flask.palletsprojects.com/) |
| **Frontend** | HTML5, CSS3, [Bootstrap 5](https://getbootstrap.com/), [JavaScript (ES6)](https://developer.mozilla.org/en-US/docs/Web/JavaScript) |
| **API** | [OpenWeatherMap API](https://openweathermap.org/api) |
| **Maps** | [Leaflet.js](https://leafletjs.com/) |
| **Hosting (optional)** | [Render](https://render.com/) / [Railway](https://railway.app/) / [Vercel](https://vercel.com/) |

---

## ⚙️ Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/<your-username>/weather-app.git
cd weather-app
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
pip install -r requirements.txt
API_KEY=60efbddb88dd2481343c67fc1140524c
python app.py
weather_app/
│
├── static/
│   ├── default.jpg
│   └── (optional background images)
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
└── README.md
![Weather App Screenshot](static/screenshot.png)

---

Would you like me to make it **auto-generate a screenshot preview** (using your local app and a tool like `flask_apscheduler` or `selenium` to render it) so you can attach an actual image for GitHub display?


