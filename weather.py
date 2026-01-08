import tkinter as tk
import requests

def get_coordinates(city):
    # Only search in the United States
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1&countrycodes=US"
    headers = {"User-Agent": "weather-app-2026"}  # required by Nominatim
    try:
        response = requests.get(url, headers=headers, timeout=5).json()
        if response:
            return float(response[0]["lat"]), float(response[0]["lon"])
    except:
        pass
    return None, None


def get_weather(event = None):
    city = city_entry.get().strip()
    if not city:
        weather_text.set("Please enter a city name!")
        return

    lat, lon = get_coordinates(city)
    if lat is None:
        weather_text.set("City not found!")
        return

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=fahrenheit"
    
    try:
        data = requests.get(url).json()
        weather = data["current_weather"]
        weather_text.set(
            f"🌤️ {city} Weather Right Now:\n"
            f"Temp: {weather['temperature']}°F\n"
            f"Wind: {weather['windspeed']} mph\n"
            f"Direction: {weather['winddirection']}°\n"
            f"Time: {weather['time']}"
        )
    except:
        weather_text.set("Error fetching weather.")

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Weather App")

tk.Label(root, text="Enter city:", font=("Arial", 12)).pack(pady=(10, 0))
city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=(0, 10))
city_entry.bind("<Return>", get_weather)  # <-- add this line


weather_text = tk.StringVar()
weather_label = tk.Label(root, textvariable=weather_text, font=("Arial", 14), justify="left")
weather_label.pack(padx=20, pady=20)

refresh_button = tk.Button(root, text="Get Weather", command=get_weather)
refresh_button.pack(pady=10)

# Start app
root.mainloop()
