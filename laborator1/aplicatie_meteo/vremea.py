import sys
import urllib.request
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def get_coordinates(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ro&format=json"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    if not data.get("results"):
        print(f"Orasul '{city}' nu a fost gasit.")
        sys.exit(1)
    result = data["results"][0]
    return result["latitude"], result["longitude"], result.get("name", city), result.get("country", "")


def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data["current_weather"]


def get_weather_code_description(code):
    descriptions = {
        0: "Cer senin",
        1: "Predominant senin",
        2: "Partial noros",
        3: "Acoperit",
        45: "Ceata",
        48: "Depunere de chiciura",
        51: "Burnita usoara",
        53: "Burnita moderata",
        55: "Burnita densa",
        56: "Burnita inghetata usoara",
        57: "Burnita inghetata densa",
        61: "Ploaie usoara",
        63: "Ploaie moderata",
        65: "Ploaie puternica",
        66: "Ploaie inghetata usoara",
        67: "Ploaie inghetata puternica",
        71: "Ninsoare usoara",
        73: "Ninsoare moderata",
        75: "Ninsoare puternica",
        77: "Grindina",
        80: "Averse usoare",
        81: "Averse moderate",
        82: "Averse puternice",
        85: "Averse de ninsoare usoare",
        86: "Averse de ninsoare puternice",
        95: "Furtuna",
        96: "Furtuna cu grindina usoara",
        99: "Furtuna cu grindina puternica",
    }
    return descriptions.get(code, "Necunoscut")


def get_wind_direction(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SV", "V", "NV"]
    index = round(degrees / 45) % 8
    return directions[index]


def main():
    city = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Introdu numele orasului: ")

    lat, lon, name, country = get_coordinates(city)
    weather = get_weather(lat, lon)

    temp = weather["temperature"]
    wind_speed = weather["windspeed"]
    wind_dir = get_wind_direction(weather.get("winddirection", 0))
    code = weather["weathercode"]
    desc = get_weather_code_description(code)

    print(f"\nVremea in {name}, {country}")
    print("=" * 40)
    print(f"  Temperatura:     {temp}°C")
    print(f"  Descriere:       {desc}")
    print(f"  Vant:            {wind_speed} km/h, directia {wind_dir}")
    print("=" * 40)


if __name__ == "__main__":
    main()
