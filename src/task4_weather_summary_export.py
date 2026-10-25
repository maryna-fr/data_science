import csv

try:
    from src.utils import load_json
except ImportError:
    from utils import load_json

HOT_THRESHOLD = 30.0
WIND_THRESHOLD = 15.0

HEADERS = [
    "Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed",
    "Humidity", "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day",
]


def summarize_weather_data(daily_data: list) -> dict:
    n = len(daily_data)
    if n == 0:
        return {}
    return {
        "average_max_temp": sum(d["max_temperature"] for d in daily_data) / n,
        "average_min_temp": sum(d["min_temperature"] for d in daily_data) / n,
        "total_precipitation": sum(d["precipitation"] for d in daily_data),
        "average_wind_speed": sum(d["wind_speed"] for d in daily_data) / n,
        "average_humidity": sum(d["humidity"] for d in daily_data) / n,
        "hot_days": sum(1 for d in daily_data if d["max_temperature"] > HOT_THRESHOLD),
        "windy_days": sum(1 for d in daily_data if d["wind_speed"] > WIND_THRESHOLD),
        "rainy_days": sum(1 for d in daily_data if d["precipitation"] > 0),
    }


def _write_rows(daily_data: list, file_obj) -> None:
    writer = csv.writer(file_obj)
    writer.writerow(HEADERS)
    for d in daily_data:
        writer.writerow([
            d["date"],
            d["max_temperature"],
            d["min_temperature"],
            d["precipitation"],
            d["wind_speed"],
            d["humidity"],
            d["weather_description"],
            d["max_temperature"] > HOT_THRESHOLD,
            d["wind_speed"] > WIND_THRESHOLD,
            d["precipitation"] > 0,
        ])


def export_to_csv(daily_data: list, destination) -> None:
    """destination: file path (str) or file-like object (e.g. StringIO)."""
    if isinstance(destination, str):
        with open(destination, "w", newline="", encoding="utf-8") as f:
            _write_rows(daily_data, f)
    else:
        _write_rows(daily_data, destination)


def main() -> None:
    data = load_json("src/tokyo_weather_complex.json")
    daily = data["daily"]
    print(summarize_weather_data(daily))
    export_to_csv(daily, "weather_summary.csv")


if __name__ == "__main__":
    main()