from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Функция для получения данных о погоде
def get_weather(city):
    api_key = '95a6fdb82d4f7e65c88dc36e2a95ad0d'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric&lang=ru"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError):
        return None

# Функция для получения новостей
def get_news():
    api_key = '40d7311202e340b1b6803588f937864a'
    url = f"https://newsapi.org/v2/top-headlines?country=ru&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError):
        return None

# Функция для получения случайной цитаты
def get_quote():
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        quote_data = response.json()[0]
        return {"content": quote_data['q'], "author": quote_data['a']}
    except (requests.exceptions.RequestException, ValueError):
        return {"content": "Сервис цитат недоступен", "author": ""}

@app.route('/', methods=['GET', 'POST'])
def home():
    city = "Москва"
    if request.method == 'POST':
        city = request.form.get('city', 'Москва')

    weather_data = get_weather(city)
    news_data = get_news()
    quote_data = get_quote()

    return render_template("index.html", weather=weather_data, news=news_data.get('articles', []), quote=quote_data, city=city)

if __name__ == "__main__":
    app.run(debug=True)
