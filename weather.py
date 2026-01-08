import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

APP_TITLE = "Weather App"
FAVORITES_FILE = "favorites.json"
HEADERS = {"User-Agent": "weather-app-2026"}

# ------------------ Data Helpers ------------------

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f)

# ------------------ API Helpers ------------------

def get_coordinates(city):
    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={city}&format=json&limit=1&countrycodes=US"
    )
    try:
        res = requests.get(url, headers=HEADERS, timeout=5).json()
        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])
    except:
        pass
    return None, None

def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true"
        "&temperature_unit=fahrenheit"
    )
    res = requests.get(url, timeout=5)
    return res.json()["current_weather"]

# ------------------ UI Logic ------------------

def set_loading(state=True):
    weather_text.set("Loading..." if state else "")

def get_weather(event=None):
    city = city_entry.get().strip()

    if not city:
        weather_text.set("Please enter a city.")
        return

    set_loading(True)
    root.update()

    lat, lon = get_coordinates(city)
    if lat is None:
        weather_text.set("City not found.")
        return

    try:
        weather = fetch_weather(lat, lon)

        weather_text.set(
            f"Weather in {city}\n\n"
            f"Temp: {weather['temperature']}°F\n"
            f"Wind: {weather['windspeed']} mph\n"
            f"Direction: {weather['winddirection']}°\n"
            f"Updated: {weather['time']}"
        )

        add_recent(city)

    except:
        weather_text.set("Error fetching weather.")

def add_favorite():
    city = city_entry.get().strip()
    if not city:
        return

    if city not in favorites:
        favorites.append(city)
        save_favorites(favorites)
        favorites_list.insert(tk.END, city)

def clear_favorites():
    favorites.clear()                  # Clear memory
    save_favorites(favorites)          # Clear disk
    favorites_list.delete(0, tk.END)   # Clear UI
    messagebox.showinfo("Favorites", "All favorites cleared!")

def load_favorite(event):
    selection = favorites_list.curselection()
    if selection:
        city = favorites_list.get(selection[0])
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        get_weather()

def add_recent(city):
    if city not in recent:
        recent.insert(0, city)
        if len(recent) > 5:
            recent.pop()

        recent_list.delete(0, tk.END)
        for c in recent:
            recent_list.insert(tk.END, c)

def load_recent(event):
    selection = recent_list.curselection()
    if selection:
        city = recent_list.get(selection[0])
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        get_weather()

# ------------------ App Setup ------------------

root = tk.Tk()
root.title(APP_TITLE)
root.geometry("420x520")
root.resizable(False, False)

favorites = load_favorites()
recent = []

# ------------------ UI Layout ------------------

tk.Label(root, text="Enter City", font=("Arial", 12)).pack(pady=(10, 0))

city_entry = tk.Entry(root, font=("Arial", 12), justify="center")
city_entry.pack(pady=5)
city_entry.bind("<Return>", get_weather)

tk.Button(root, text="Get Weather", command=get_weather).pack(pady=5)
tk.Button(root, text="Add to Favorites", command=add_favorite).pack(pady=5)
tk.Button(root, text="Clear Favorites", command=clear_favorites).pack(pady=5)

weather_text = tk.StringVar()
tk.Label(
    root,
    textvariable=weather_text,
    font=("Arial", 13),
    justify="left",
    wraplength=380
).pack(padx=20, pady=15)

# Favorites
tk.Label(root, text="Favorites", font=("Arial", 11, "bold")).pack()
favorites_list = tk.Listbox(root, height=4)
favorites_list.pack(padx=20, fill="x")
favorites_list.bind("<<ListboxSelect>>", load_favorite)

for city in favorites:
    favorites_list.insert(tk.END, city)

# Recent
tk.Label(root, text="Recent Searches", font=("Arial", 11, "bold")).pack(pady=(10, 0))
recent_list = tk.Listbox(root, height=4)
recent_list.pack(padx=20, fill="x")
recent_list.bind("<<ListboxSelect>>", load_recent)

# ------------------ Start ------------------

root.mainloop()
