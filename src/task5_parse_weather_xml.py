import csv
import xml.etree.ElementTree as ET

XML_FILE = "src/weather_data.xml"
OUTPUT_FILE = "parsed_weather_data.csv"
HEADERS = ["Date", "Temperature", "Humidity", "Precipitation"]


def parse_weather_xml(xml_path: str = XML_FILE) -> list:
    root = ET.parse(xml_path).getroot()
    result = []
    for day in root.findall("day"):
        result.append({
            "date": day.findtext("date", default="").strip(),
            "temperature": float(day.findtext("temperature")),
            "humidity": int(float(day.findtext("humidity"))),
            "precipitation": float(day.findtext("precipitation")),
        })
    return result


def save_to_csv(data: list, filename: str = OUTPUT_FILE) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for row in data:
            writer.writerow([
                row["date"], row["temperature"], row["humidity"], row["precipitation"],
            ])


def main() -> None:
    save_to_csv(parse_weather_xml())


if __name__ == "__main__":
    main()