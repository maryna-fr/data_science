import csv
import re

TEXT_FILE = "src/weather_report.txt"
OUTPUT_FILE = "extracted_weather_data.csv"
HEADERS = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]

PATTERN = re.compile(
    r"Date:\s*(\d{4}-\d{2}-\d{2}),\s*"
    r"Max Temp:\s*(-?\d+(?:\.\d+)?)\s*C,\s*"
    r"Min Temp:\s*(-?\d+(?:\.\d+)?)\s*C,\s*"
    r"Humidity:\s*(\d+(?:\.\d+)?)\s*%,\s*"
    r"Precipitation:\s*(-?\d+(?:\.\d+)?)\s*mm"
)


def clean_text(text: str) -> str:
    """Remove non-ASCII characters (degree sign, broken encodings)."""
    return text.encode("ascii", "ignore").decode("ascii")


def extract_weather_data(file_path: str = TEXT_FILE) -> list:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    result = []
    for line in clean_text(text).splitlines():
        match = PATTERN.search(line)
        if match:
            date, max_t, min_t, humidity, precip = match.groups()
            result.append({
                "date": date,
                "max_temperature": float(max_t),
                "min_temperature": float(min_t),
                "humidity": int(float(humidity)),
                "precipitation": float(precip),
            })
    return result


def save_to_csv(data: list, filename: str = OUTPUT_FILE) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for row in data:
            writer.writerow([
                row["date"], row["max_temperature"], row["min_temperature"],
                row["humidity"], row["precipitation"],
            ])


def main() -> None:
    save_to_csv(extract_weather_data())


if __name__ == "__main__":
    main()