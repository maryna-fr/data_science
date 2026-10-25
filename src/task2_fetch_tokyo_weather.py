import requests

try:
    from src.utils import save_to_json
except ImportError:
    from utils import save_to_json

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=35.6895&longitude=139.6917"
    "&daily=temperature_2m_max&timezone=Asia/Tokyo"
)
OUTPUT_FILE = "tokyo_weather.json"


def fetch_weather_data(url: str = API_URL) -> dict:
    """Fetch the forecast and return the date and max temperature."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    daily = response.json()["daily"]
    return {
        "date": daily["time"][0],
        "max_temperature": daily["temperature_2m_max"][0],
    }


def main() -> None:
    save_to_json(fetch_weather_data(), OUTPUT_FILE)


if __name__ == "__main__":
    main()