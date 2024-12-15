import speech_recognition as sr
import pyttsx3
import webbrowser
# import requests as r (Uncomment it when want to get news)
from openai import OpenAI

# Initialize the text-to-speech engine
engine = pyttsx3.init()
# OpenAI API key
# openai.api_key = " Your api key"

def ask_openai(prompt):
    """Use OpenAI's GPT to generate a response to a given prompt."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can use other models like gpt-4
            prompt=prompt,
            max_tokens=150,  # Limit the response length
            temperature=0.7  # Control response randomness
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "Sorry, I couldn't process your request with OpenAI."
    pass #Delete this pass when using open AI

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a dictionary of songs with their respective URLs
music = {
    "skyfall": "https://youtu.be/DeumyOzKqgI?feature=shared",
    "whoopty": "https://youtu.be/2xWkATdMQms?feature=shared",
    "millionaire": "https://youtu.be/XO8wew38VM8?feature=shared",
    "bonita": "https://youtu.be/q3EsYvIapPQ?feature=shared"
}

# Function to fetch and read news headlines
# def get_news(country=(Give your country name)):
#     API_KEY = "Your API KEY"  # Replace with your NewsAPI key
#     url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}"
#     try:
#         response = r.get(url)
#         news_data = response.json()
#         if news_data.get("status") == "ok" and news_data.get("articles"):
#             articles = news_data["articles"][:5]  # Get top 5 headlines
#             speak("Here are the latest news headlines.")
#             for i, article in enumerate(articles, 1):
#                 headline = article.get("title", "No title available")
#                 print(f"News {i}: {headline}")
#                 speak(f"News {i}: {headline}")
#         else:
#             speak("Sorry, no news articles are available at the moment.")
#     except Exception as e:
#         print(f"Error fetching news: {e}")
#         speak("Sorry, I encountered an error while fetching the news.")

# Function to process voice commands
def process_command(command):
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open x" in command:
        speak("Opening X")
        webbrowser.open("https://x.com")
    elif "news" in command:
        if "for" in command:
            country = command.split("for")[-1].strip().lower()[:2]  # Extract country code
            speak(f"Fetching news for {country.upper()}.")
            get_news(country)
        else:
            speak("Fetching news for the United States.")
            get_news()  # Default to US news
        pass # Delete this pass once you give your country name and API
    elif command.startswith("play "):
        song = command.split("play ", 1)[1].strip()  # Takes everything after "play"
        if song in music:
            speak(f"Playing {song}")
            webbrowser.open(music[song])
        else:
            speak(f"Sorry, I couldn't find the song {song}. Available songs are {', '.join(music.keys())}.")
    elif "what is" in command or "who is" in command or "explain" in command:
        # Use OpenAI to answer general questions
        speak("Let me check that for you.")
        answer = ask_openai(command)
        print(f"OpenAI response: {answer}")
        speak(answer)
    else:
        speak("Sorry, I didn't understand the command.")


if __name__ == "__main__":
    speak("Hey Sir, I am your Assistant. I am here to help you.")
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("Listening for your commands. Say 'exit' to stop.")
        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)  # Continuous listening
                
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                
                if command.lower() == "exit":
                    speak("Goodbye, sir.")
                    break  # Exit the program
                elif "jarvis" in command.lower():
                    speak("Yes sir, I am listening.")
                else:
                    process_command(command)
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                speak("Sorry, there seems to be a connection problem.")
