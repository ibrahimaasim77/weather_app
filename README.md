Weather App
A simple and professional Tkinter-based weather application in Python that lets users search for U.S. cities, view live weather data, and manage favorites and recent searches. Built as a portfolio project to demonstrate API integration, state management, and GUI design.
Features
Search any U.S. city to view the current temperature, wind speed, wind direction, and update time.
Favorites list: save your frequently searched cities; data persists across app restarts.
Clear Favorites button: remove all favorites at once.
Recent Searches: track the last 5 cities you searched in the current session.
Clean, professional UI with easy-to-read fonts and intuitive layout.
Error handling: handles invalid city names or API errors gracefully.
Installation
Clone the repository
git clone https://github.com/ibrahimaasim77/weather-app.git
cd weather-app
Create a Python virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
Install dependencies
pip install requests
Run the app
python weather_app.py
Usage
Enter a city name in the input field and click Get Weather.
Add a city to Favorites using the button.
Select a city from Favorites or Recent Searches to quickly view its weather.
Use Clear Favorites to remove all saved cities.
Screenshots
(Optional: add screenshots of your app here for portfolio visibility)
Technical Details
Language: Python 3
GUI: Tkinter
APIs Used:
OpenStreetMap Nominatim API for geocoding
Open-Meteo API for weather data
Data Persistence: JSON file for favorites (favorites.json)
Future Improvements
Add Clear Recent Searches button
Support for 5-day forecast
Switch between Fahrenheit/Celsius
Add dark mode for better UX
Package as a standalone executable using PyInstaller
Author
Ibrahim Aasim
Portfolio / GitHub: https://github.com/ibrahimaasim77
Python & Tkinter projects | Road to FAANG
