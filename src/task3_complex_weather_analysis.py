try:
    from src.utils import load_json
except ImportError:
    from utils import load_json

HOT_THRESHOLD = 30.0
SWING_THRESHOLD = 10.0
WIND_THRESHOLD = 15.0
HUMIDITY_THRESHOLD = 70.0

DEGREE = "\u00b0"


def rain_severity(precipitation: float) -> str:
    if precipitation <= 0:
        return "none"
    if precipitation <= 5:
        return "light"
    if precipitation <= 10:
        return "moderate"
    return "heavy"


def analyze_daily_weather(day: dict) -> dict:
    max_t = day["max_temperature"]
    min_t = day["min_temperature"]
    swing = round(max_t - min_t, 1)
    return {
        "date": day["date"],
        "weather_description": day.get("weather_description", ""),
        "max_temperature": max_t,
        "min_temperature": min_t,
        "is_hot_day": max_t > HOT_THRESHOLD,
        "temperature_swing": swing,
        "is_significant_swing": swing > SWING_THRESHOLD,
        "wind_speed": day["wind_speed"],
        "is_windy_day": day["wind_speed"] > WIND_THRESHOLD,
        "humidity": day["humidity"],
        "is_uncomfortable_day": day["humidity"] > HUMIDITY_THRESHOLD,
        "precipitation": day["precipitation"],
        "is_rainy_day": day["precipitation"] > 0,
        "rain_severity": rain_severity(day["precipitation"]),
    }


def generate_daily_report(analysis: dict) -> str:
    lines = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis.get('weather_description', '')}",
        (
            f"Temperature: Max {analysis['max_temperature']}{DEGREE}C, "
            f"Min {analysis['min_temperature']}{DEGREE}C "
            f"(Swing: {analysis['temperature_swing']}{DEGREE}C)"
        ),
    ]
    if analysis["is_hot_day"]:
        lines.append("It was a hot day.")
    if analysis.get("is_significant_swing"):
        lines.append("There was a significant temperature swing.")
    if analysis["is_windy_day"]:
        lines.append("It was a windy day.")
    if analysis["is_uncomfortable_day"]:
        lines.append("The humidity made the day uncomfortable.")
    if analysis["is_rainy_day"]:
        lines.append("It was a rainy day.")
    else:
        lines.append("There was no precipitation.")
    return "\n".join(lines)


def summarize_weather_analysis(analyses: list) -> str:
    hottest = max(analyses, key=lambda a: a["max_temperature"])
    windiest = max(analyses, key=lambda a: a["wind_speed"])
    humid = max(analyses, key=lambda a: a["humidity"])
    rainiest = max(analyses, key=lambda a: a["precipitation"])
    return "\n".join([
        "Weather Summary:",
        f"Hottest day: {hottest['date']} with a maximum temperature of {hottest['max_temperature']}{DEGREE}C",
        f"Windiest day: {windiest['date']} with wind speeds of {windiest['wind_speed']} km/h",
        f"Most humid day: {humid['date']} with a humidity level of {humid['humidity']}%",
        f"Rainiest day: {rainiest['date']} with {rainiest['precipitation']} mm of precipitation",
    ])


def main() -> None:
    data = load_json("src/tokyo_weather_complex.json")
    analyses = [analyze_daily_weather(day) for day in data["daily"]]
    for analysis in analyses:
        print(generate_daily_report(analysis))
        print()
    print(summarize_weather_analysis(analyses))


if __name__ == "__main__":
    main()