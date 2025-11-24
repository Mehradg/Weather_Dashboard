import requests
import json 

api_key = "7e51f2232fa894c54aee2f523f8011c9"
temperature = None
humidity = None
description = None 
def save_weather_data(city, temperature, humidity, description):
    weather_record = {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "condition": description
    }
    
    with open("weather_data.json", "a") as file:
        json.dump(weather_record, file)
        file.write("\n") 

    print("Weather data saved!")

def get_weather(city):
    
    global temperature, humidity, description
    city = city.strip()
    if not city:
        print("City name cannot be empty.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        weather_data = response.json()
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]
        print(f"Weather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Condition: {description}")
    except Exception as e:
        print(f"Error while fetching weather data: {e}")
        return


def view_past_weather():
    
    try:
        with open("weather_data.json", "r") as file:
            lines = file.readlines()

        if not lines:
            print("No past weather data found yet.")
            return

        print("\nPast Weather Searches:")
        for i, line in enumerate(lines, start=1):
            try:
                record = json.loads(line.strip())
                city = record.get("city", "Unknown")
                temp = record.get("temperature", "?")
                hum = record.get("humidity", "?")
                cond = record.get("condition", "?")
                print(f"{i}. {city} | {temp}°C | {hum}% | {cond}")
            except json.JSONDecodeError:
                print(f"{i}. (Corrupted record)")
    except FileNotFoundError:
        print("No past weather data file found yet. Do a search first!")

def menu():
    while True:
        print("\n Weather Dashboard")
        print("1. Get Current Weather")
        print("2. View Past Searches")
        print("3. Exit")
        
        choice = input("Choose an option: ")
 
        if choice == "1":
            city = input("Enter city name: ")
            get_weather(city)
            ask_user = input("Do you want to save this data? (y/n): ").lower()
            if ask_user == 'y':  
                save_weather_data(city, temperature, humidity, description)
        elif choice == "2":
            view_past_weather()  
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
 
menu()

