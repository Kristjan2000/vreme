from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_KEY = "511e6c0bc1fbfd53c2629ec9edfb60ae"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form.get("city")
        complete_url = f"{BASE_URL}?q={city}&units=metric&appid={API_KEY}"
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] == 200:
            main_data = data["main"]
            weather_data = data["weather"][0]
            temperature = main_data["temp"]

            weather_description = weather_data["description"]
            return render_template_string("""
                <h1>Vreme v {{city}}</h1>
                <p>Temperatura: {{temp}}°C</p>
                <p>Opis vremena: {{description}}</p>
                <br>
                <a href="/">Nazaj</a>
            """, city=city, temp=temperature, description=weather_description)
        else:
            return "<h1>Mesta ni bilo mogoče najti.</h1>"

    return """
        <form method="POST">
            Enter city name:<br>
            <input type="text" name="city" required><br>
            <input type="submit" value="Get Weather">
        </form>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
