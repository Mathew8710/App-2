import openai
import config
import requests
import datetime
import webbrowser
import pytz

openai.api_key = config.OPENAI_API_KEY

conversation_history = []

def handle_command(command):
    command = command.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if any(command == greet or command.startswith(greet + " ") or command.endswith(" " + greet) or (" " + greet + " ") in command for greet in greetings):
        return "Hello! How can I assist you today?"

    if "time in" in command:
        # Extract location after "time in"
        location = command.split("time in",1)[1].strip()
        return get_time_in_location(location)

    if "time" in command:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."

    if "news" in command:
        return get_news()

    if command.startswith("open "):
        site = command[len("open "):].strip()
        website_mapping = {
            "youtube": "https://www.youtube.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "outlook": "https://outlook.live.com",
            "gmail": "https://mail.google.com",
            "netflix": "https://www.netflix.com",
            "hotstar": "https://www.hotstar.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            "github": "https://github.com",
            "stackoverflow": "https://stackoverflow.com",
            "google": "https://www.google.com",
            "amazon": "https://www.amazon.com",
            "ebay": "https://www.ebay.com",
            "wikipedia": "https://www.wikipedia.org"
        }
        url = website_mapping.get(site)
        if url:
            webbrowser.open(url)
            return f"Opening {site.title()}."
        else:
            return f"Sorry, I don't have the website {site} in my list."

    # Generic website opener
    if command.startswith("open "):
        site = command[len("open "):].strip()
        website_mapping = {
            "youtube": "https://www.youtube.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "outlook": "https://outlook.live.com",
            "gmail": "https://mail.google.com",
            "netflix": "https://www.netflix.com",
            "hotstar": "https://www.hotstar.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            "github": "https://github.com",
            "stackoverflow": "https://stackoverflow.com",
            "google": "https://www.google.com",
            "amazon": "https://www.amazon.com",
            "ebay": "https://www.ebay.com",
            "wikipedia": "https://www.wikipedia.org"
        }
        url = website_mapping.get(site)
        if url:
            webbrowser.open(url)
            return f"Opening {site.title()}."
        else:
            return f"Sorry, I don't have the website {site} in my list."

    if command.startswith("search "):
        query = command[len("search "):]
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching Google for {query}."

    if "weather" in command:
        # Extract location if specified
        words = command.split()
        location = "London"  # default location
        if "in" in words:
            in_index = words.index("in")
            if in_index + 1 < len(words):
                location = " ".join(words[in_index + 1:])
        return get_weather(location)

    if command in ["exit", "quit", "stop"]:
        return "Goodbye!"

    # Use OpenAI GPT for other queries with conversation memory
    conversation_history.append(f"User: {command}")
    response = ask_openai("\n".join(conversation_history))
    conversation_history.append(f"Assistant: {response}")
    # Limit conversation history to last 10 exchanges (20 lines)
    if len(conversation_history) > 20:
        conversation_history.pop(0)
        conversation_history.pop(0)
    return response

def get_weather(location):
    # Example: Use OpenWeatherMap API (user must add API key in config)
    if not config.OPENWEATHER_API_KEY:
        return "Weather API key is not configured."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={config.OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("weather"):
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The weather in {location} is {description} with a temperature of {temp}°C."
        else:
            return "Sorry, I could not get the weather information."
    except Exception as e:
        return "Failed to get weather data."

def get_news():
    if not hasattr(config, 'NEWS_API_KEY') or not config.NEWS_API_KEY or config.NEWS_API_KEY == "your_news_api_key_here":
        return "News API key is not configured."
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={config.NEWS_API_KEY}&pageSize=5"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("articles"):
            articles = data["articles"]
            headlines = [article["title"] for article in articles]
            return "Here are the top news headlines: " + "; ".join(headlines)
        else:
            return "Sorry, I could not get the news information."
    except Exception as e:
        return "Failed to get news data."

def get_time_in_location(location):
    try:
        # Use pytz to get timezone from location
        # This is a simple mapping for demo; in real use, a more comprehensive mapping or API is recommended
        timezone_mapping = {
            "new york": "America/New_York",
            "los angeles": "America/Los_Angeles",
            "london": "Europe/London",
            "paris": "Europe/Paris",
            "tokyo": "Asia/Tokyo",
            "delhi": "Asia/Kolkata",
            "sydney": "Australia/Sydney",
            "berlin": "Europe/Berlin",
            "moscow": "Europe/Moscow",
            "dubai": "Asia/Dubai",
            "beijing": "Asia/Shanghai",
            "singapore": "Asia/Singapore",
            "cairo": "Africa/Cairo",
            "rio de janeiro": "America/Sao_Paulo"
        }
        tz_name = timezone_mapping.get(location.lower())
        if not tz_name:
            return f"Sorry, I don't have timezone information for {location}."
        tz = pytz.timezone(tz_name)
        time_in_location = datetime.datetime.now(tz)
        return f"The current time in {location.title()} is {time_in_location.strftime('%I:%M %p')}."
    except Exception as e:
        return "Sorry, I couldn't get the time for that location."

def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return "Sorry, I am unable to process your request right now."
