import requests   #pip install requests before running
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime, timedelta, timezone

# API keys for weather and timezone services
WEATHER_API_KEY = "b7e316d0a50c2cf1fe2c1a0c56216cc7"    #for weather this api
TIMEZONE_API_KEY = "V9UHTNGNX9EQ"  #for current time use this api

# A global variable to store the timezone offset for calculating local time
timezone_offset = 0

class WeatherApp:
    def __init__(self, root):
        """
        Initializes the WeatherApp GUI with input, display, and forecast sections.
        """
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")
        self.root.configure(bg="#F0F0F0")  # Set a neutral background color

        # Input section for the user to enter the city name
        self.input_frame = tk.Frame(root, bg="#F0F0F0", padx=10, pady=10)
        self.input_frame.pack(fill=tk.X)

        self.city_label = tk.Label(self.input_frame, text="Enter City Name:", bg="#F0F0F0", font=("Arial", 12))
        self.city_label.pack(side=tk.LEFT, padx=5)

        self.city_entry = tk.Entry(self.input_frame, width=30, font=("Arial", 12))
        self.city_entry.pack(side=tk.LEFT, padx=5)

        self.get_weather_btn = tk.Button(self.input_frame, text="Get Weather", command=self.get_weather, font=("Arial", 12))
        self.get_weather_btn.pack(side=tk.LEFT, padx=5)

        # Display section for current weather details
        self.display_frame = tk.Frame(root, bg="#F0F0F0", padx=10, pady=10)
        self.display_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Labels for displaying weather information
        self.city_name_label = tk.Label(self.display_frame, text="City Name:", bg="#F0F0F0", font=("Arial", 14, "bold"))
        self.city_name_label.pack(anchor=tk.W, pady=5)

        self.temperature_label = tk.Label(self.display_frame, text="Temperature:", bg="#F0F0F0", font=("Arial", 12))
        self.temperature_label.pack(anchor=tk.W, pady=5)

        self.weather_desc_label = tk.Label(self.display_frame, text="Weather Description:", bg="#F0F0F0", font=("Arial", 12))
        self.weather_desc_label.pack(anchor=tk.W, pady=5)

        self.wind_speed_label = tk.Label(self.display_frame, text="Wind Speed:", bg="#F0F0F0", font=("Arial", 12))
        self.wind_speed_label.pack(anchor=tk.W, pady=5)

        self.humidity_label = tk.Label(self.display_frame, text="Humidity:", bg="#F0F0F0", font=("Arial", 12))
        self.humidity_label.pack(anchor=tk.W, pady=5)

        self.last_update_label = tk.Label(self.display_frame, text="Last Update:", bg="#F0F0F0", font=("Arial", 12))
        self.last_update_label.pack(anchor=tk.W, pady=5)

        self.timezone_label = tk.Label(self.display_frame, text="Timezone:", bg="#F0F0F0", font=("Arial", 12))
        self.timezone_label.pack(anchor=tk.W, pady=5)

        self.current_time_label = tk.Label(self.display_frame, text="Current Time:", bg="#F0F0F0", font=("Arial", 12))
        self.current_time_label.pack(anchor=tk.W, pady=5)

        self.time_of_day_label = tk.Label(self.display_frame, text="Time of Day:", bg="#F0F0F0", font=("Arial", 12))
        self.time_of_day_label.pack(anchor=tk.W, pady=5)

        # Placeholder for the weather icon
        self.weather_icon_label = tk.Label(self.display_frame, bg="#F0F0F0")
        self.weather_icon_label.pack(pady=10)

        # Forecast section for the next 3 days
        self.forecast_frame = tk.Frame(root, bg="#F0F0F0", padx=10, pady=10)
        self.forecast_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        self.forecast_title = tk.Label(self.forecast_frame, text="3-Day Forecast", bg="#F0F0F0", font=("Arial", 14, "bold"))
        self.forecast_title.pack(anchor=tk.W, pady=5)

        # Create frames for each forecast day
        self.forecast_boxes = []
        self.forecast_labels = []
        self.forecast_icons = []
        for _ in range(3):
            forecast_box = tk.Frame(self.forecast_frame, bg="#F0F0F0", relief="solid", bd=2, padx=10, pady=10)
            forecast_box.pack(fill=tk.X, pady=5)
            self.forecast_boxes.append(forecast_box)

            label = tk.Label(forecast_box, text="", bg="#F0F0F0", font=("Arial", 12))
            label.pack(anchor=tk.W, pady=5)
            self.forecast_labels.append(label)

            icon_label = tk.Label(forecast_box, bg="#F0F0F0")
            icon_label.pack(pady=5)
            self.forecast_icons.append(icon_label)

    def get_weather(self):
        """
        Fetches the current weather and 3-day forecast data for the given city.
        """
        city = self.city_entry.get().strip()

        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        try:
            # Fetch weather details
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            weather_response = requests.get(weather_url).json()

            if weather_response.get("cod") != 200:
                messagebox.showerror("Error", weather_response.get("message", "Failed to fetch weather data."))
                return

            # Parse weather details
            city_name = weather_response["name"]
            temperature = weather_response["main"]["temp"]
            weather_desc = weather_response["weather"][0]["description"]
            weather_code = weather_response["weather"][0]["icon"]
            wind_speed = weather_response["wind"]["speed"]
            humidity = weather_response["main"]["humidity"]
            last_update_unix = weather_response["dt"]
            latitude = weather_response["coord"]["lat"]
            longitude = weather_response["coord"]["lon"]

            # Update the GUI with weather information
            self.city_name_label.config(text=f"City Name: {city_name}")
            self.temperature_label.config(text=f"Temperature: {temperature} °C")
            self.weather_desc_label.config(text=f"Weather Description: {weather_desc}")
            self.wind_speed_label.config(text=f"Wind Speed: {wind_speed} m/s")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.last_update_label.config(text=f"Last Update: {datetime.fromtimestamp(last_update_unix, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")

            # Fetch timezone information
            timezone_url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={TIMEZONE_API_KEY}&format=json&by=position&lat={latitude}&lng={longitude}"
            timezone_response = requests.get(timezone_url).json()

            global timezone_offset
            timezone_offset = timezone_response["gmtOffset"]
            timezone_name = timezone_response["zoneName"]
            self.timezone_label.config(text=f"Timezone: {timezone_name}")

            # Display local time
            self.display_time_in_timezone()

            # Fetch and display the weather icon
            self.display_weather_icon(weather_code)

            # Fetch 3-day forecast
            self.get_forecast(city)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_time_in_timezone(self):
        """
        Calculates and displays the local time based on the timezone offset.
        """
        current_time = datetime.now(timezone.utc) + timedelta(seconds=timezone_offset)
        self.current_time_label.config(text=f"Current Time: {current_time.strftime('%I:%M:%S %p')}")
        self.time_of_day_label.config(text=f"Time of Day: {self.determine_time_of_day(current_time)}")

    def determine_time_of_day(self, current_time):
        """
        Returns a time-of-day label based on the current hour.
        """
        hour = current_time.hour
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        elif 18 <= hour < 21:
            return "Evening"
        else:
            return "Night"

    def display_weather_icon(self, weather_code):
        """
        Fetches and displays the weather icon based on the code.
        """
        try:
            icon_url = f"http://openweathermap.org/img/wn/{weather_code}.png"
            response = requests.get(icon_url)
            icon_data = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(icon_data)
            self.weather_icon_label.config(image=icon_image)
            self.weather_icon_label.image = icon_image
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load weather icon: {str(e)}")

    def get_forecast(self, city):
        """
        Fetches and displays the 3-day weather forecast.
        """
        try:
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url).json()

            if forecast_response.get("cod") != "200":
                messagebox.showerror("Error", forecast_response.get("message", "Failed to fetch forecast data."))
                return

            forecasts = forecast_response["list"]
            daily_forecasts = {}

            # Extract daily forecasts for the next 3 days
            for forecast in forecasts:
                date = forecast["dt_txt"].split(" ")[0]
                if date not in daily_forecasts:
                    daily_forecasts[date] = forecast
                if len(daily_forecasts) == 3:
                    break

            for i, (date, forecast) in enumerate(daily_forecasts.items()):
                temp = forecast["main"]["temp"]
                desc = forecast["weather"][0]["description"]
                icon_code = forecast["weather"][0]["icon"]

                self.forecast_labels[i].config(text=f"{date}: {temp} °C, {desc}")
                self.display_forecast_icon(i, icon_code)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_forecast_icon(self, index, icon_code):
        """
        Fetches and displays the forecast icon for a specific day.
        """
        try:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            response = requests.get(icon_url)
            icon_data = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(icon_data)
            self.forecast_icons[index].config(image=icon_image)
            self.forecast_icons[index].image = icon_image
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load forecast icon: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()  
