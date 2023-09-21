import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer


class ZodiacSigns:
    def __init__(self):
        self.zodiac_signs = {
            "Aries": "aries",
            "Taurus": "taurus",
            "Gemini": "gemini",
            "Cancer": "cancer",
            "Leo": "leo",
            "Virgo": "virgo",
            "Libra": "libra",
            "Scorpio": "scorpio",
            "Sagittarius": "sagittarius",
            "Capricorn": "capricorn",
            "Aquarius": "aquarius",
            "Pisces": "pisces",
        }

    def get_zodiac_sign(self, sign):
        return self.zodiac_signs.get(sign)


class HoroscopeGenerator:
    def __init__(self, zodiac_signs):
        self.zodiac_signs = zodiac_signs

    def get_horoscope(self, zodiac_sign):
        url = f"https://www.exampleastrologywebsite.com/horoscope/{self.zodiac_signs.get_zodiac_sign(zodiac_sign)}.html"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception if there's an HTTP error
            soup = BeautifulSoup(response.content, "html.parser")
            horoscope_text = soup.find("div", class_="horoscope-text")
            if horoscope_text:
                return horoscope_text.get_text(strip=True)
            else:
                return None
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error accessing the website: {url}") from e

    def analyze_sentiment(self, text):
        sentences = text.split(".")
        sia = SentimentIntensityAnalyzer()
        positive_sentences = []
        negative_sentences = []

        for sentence in sentences:
            sentiment_score = sia.polarity_scores(sentence)
            if sentiment_score["compound"] > 0.2:
                positive_sentences.append(sentence.strip())
            elif sentiment_score["compound"] < -0.2:
                negative_sentences.append(sentence.strip())

        return {
            "Positive Sentences": positive_sentences,
            "Negative Sentences": negative_sentences,
        }


class AstronomyApp:
    def __init__(self):
        self.zodiac_signs = ZodiacSigns()
        self.generator = HoroscopeGenerator(self.zodiac_signs)

    def run(self):
        zodiac_sign = "Leo"
        try:
            horoscope = self.generator.get_horoscope(zodiac_sign)
            if horoscope:
                sentiment_analysis = self.generator.analyze_sentiment(horoscope)
                print(f"Horoscope for {zodiac_sign}:")
                print("-------------------------")
                print(horoscope)
                print("-------------------------")
                print("Sentiment Analysis:")
                print("-------------------------")
                print("Positive Sentences:")
                for sentence in sentiment_analysis["Positive Sentences"]:
                    print("- " + sentence)
                print("-------------------------")
                print("Negative Sentences:")
                for sentence in sentiment_analysis["Negative Sentences"]:
                    print("- " + sentence)
            else:
                print("Failed to retrieve horoscope.")
        except Exception as e:
            print("An error occurred:")
            print(str(e))


if __name__ == "__main__":
    app = AstronomyApp()
    app.run()
