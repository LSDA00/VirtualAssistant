import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import requests
import pyjokes
import wolframalpha
from newsapi import NewsApiClient
from bs4 import BeautifulSoup

# TODO:
# * Give it a good name
# * set up dict for trigger words / intents and corresponding functions
# * briefing should have spoken date along with day of the week
#   fix news in briefing so that you can respond correctly
#   Calendar events in briefing?
#
# * "how long have you been alive" - - make it recite it's age i.e how many days since creation (OS get info?)
# * you did x on this last y (week/year), would you like to do x today? (memory)
# * mac control i.e music (?)
# * diagnostic_mode mode: checking working functions + different voice
# * smart home/plug integration
# * make it so that on something like wikipedia function (AND WOLFRAM), the search term can be inside the query
#       "search for x on wikipedia", instead of "search"-"search for what"- "for x"
# * is there a better news api? You should look up docs to find out how to get just headlines for briefing
# * set up random responses

intents = {
    "greeting": ("hi", "hello", "what's up", "hey"),
    "quote": ("quote", "read me a quote", "tell me a kanye quote", "give me a kanye west quote",
              "tell me a quote from kanye west"),
    "briefing": ("briefing", "give me my briefing", "brief me", "i'd like to be briefed", "give me a briefing"),
    "news": ("news", "what's going on in the news", "what is the news like today", "is there any news", "i would like to hear the news", "tell me the news"),
    "time": ("time", "what time is it", "tell me the time", "what is the time"),
    "date": ("date", "what day is it", "what is the date", "what day of the week is it", "what day is today"),
    "weather": ("weather", "what is the weather like", "what is todays weather", "is it warm out", "is it cold out", "is it snowing", "is it raining", "how is the weather today"),
    "wikipedia": ("i want to look something up on wikipedia", "i want to search a topic on wikipedia"),
    "done": ("goodbye", "bye", "okay thank you", "thank you", "okay thats enough"),
    "name": ("name", "what is your name", "what should I call you", "do you have a name", "whats your name"),
    "wolfram": ("question", "i would like to ask you a question", "i have a question")
}

# this method is for taking the commands
# and recognizing the command from the
# speech_Recognition module we will use
# the recongizer method for recognizing
USER = "Lucas"
ASSISTANT = ", 8 OH 5"


def take_command():

    r = sr.Recognizer()
    query = " "
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio_in = r.listen(source)
            query = r.recognize_google(audio_in)
            print(query)
            print("Working on it")
        except sr.UnknownValueError:
            speak("I didn't quite catch that...")
    return query


def speak(audio):
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')

    # setter method .[0]=male voice and
    # [1]=female voice in set Property. 7, 11 stephen hawking, 17, 28, 33
    engine.setProperty('voice', voices[33].id)

    # Method for the speaking of the the ASSISTANT
    engine.say(audio)
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()


def tell_day():

    # This function is for telling the
    # day of the week
    day = datetime.datetime.today().weekday() + 1
    date = datetime.date.today()

    # this line tells us about the number
    # that will help us in telling the day
    Day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday',
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}

    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("Today is " + day_of_the_week)
        print(date)

# Gives a random Kanye west tweet


def quote():
    page = requests.get('https://api.kanye.rest')
    soup = BeautifulSoup(page.content, 'html.parser')
    quote = soup.get_text()
    print(quote)
    speak(quote + ", kanye west ")

# gives the news


def news():
    newsapi = NewsApiClient(api_key='6c7c86dad73446c08de0d273464272ab')
    speak("What would you like to hear news about?")
    topic = take_command()
    data = newsapi.get_top_headlines(
        q=topic, language="en", page_size=5)
    newsData = data["articles"]
    for y in newsData:
        speak(y["description"])


def weather():
    page = requests.get(
        "https://forecast.weather.gov/MapClick.php?textField1=45.78&textField2=-108.51#.YdjRqS-B0_U")
    soup = BeautifulSoup(page.content, 'html.parser')
    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_='tombstone-container')
    tonight = forecast_items[0]
    # print(tonight.prettify())
    period = tonight.find(class_="period-name").get_text()
    short_desc = tonight.find(class_="short-desc").get_text()
    temp = tonight.find(class_="temp").get_text()
    print(period)
    print(short_desc)
    print(temp)
    img = tonight.find("img")
    desc = img['title']
    speak(f"The weather for {desc}")


def tell_time():

    # This method will give the time
    speak("Right now it is " + datetime.datetime.now().strftime("%I:%M"))


def hello():
    hour = datetime.datetime.now().hour
    if(hour >= 0) and (hour < 12):
        speak(f"Good Morning {USER}, how can I help you?")
    elif(hour >= 12) and (hour < 18):
        speak(f"Good afternoon {USER}, how can I help you?")
    elif(hour >= 18) and (hour <= 24):
        speak(f"Good Evening {USER}, how can I help you?")


def wikipedia():
    speak("Okay, what would you like to look up on wikipedia")
    my_query = take_command().lower()
    speak(f" I am searching for {my_query}")
    my_query = my_query.replace("wikipedia", "")

    # it will give the summary of 4 lines from
    # wikipedia we can increase and decrease number of sentences
    result = wikipedia.summary(query, sentences=4)
    print(f"According to wikipedia {result}")
    speak(f"According to wikipedia {result}")


def name():
    speak(f"I am {ASSISTANT}. your virtual assistant")


def briefing():
    tell_day()
    tell_time()
    weather()
    speak("Would you like to hear the news")
    news_response = take_command().lower()
    if news_response == "yes":
        news()
    else:
        speak("Okay, have a great day!")


def diagnostic_mode():
    speak("I am ready to test greeting functionality")
    test_1 = take_command().lower()
    for i in intents["greeting"]:
        if test_1 == i:
            speak(f"greeting functionality test successful for {test_1}")
            break
        else:
            speak(f"greeting functionality test failed for {test_1}")
            print(test_1)
            print(intents["greeting"])

    speak("I am ready to test quote functionality")
    test_2 = take_command().lower()
    for j in intents["quote"]:
        if test_2 == j:
            speak(f"quote functionality test successful for {test_2}")
            break
        else:
            speak(f"quote functionality test failed for {test_2}")
            print(test_2)
            print(intents["quote"])
    test_3 = take_command.lower()
    for k in intents["wolfram"]: 
        if test_3 == k: 
            speak(f"wolfram functionality test successful for {test_3}")
            break
        else:
            speak(f"wolfram functionality test failed for {test_3}")
            print(test_3)
            print(intents["wolfram"])


def wolfram():
    # wolfram api key KXKX5E-PQPEY8W9HQ
    speak(f"Okay, what's your question {USER}?")
    user_input = take_command().lower()
    app_id = 'KXKX5E-PQPEY8W9HQ'
    client = wolframalpha.Client(app_id)
    response = client.query(user_input)
    answer = next(response.results).text
    speak(answer)


def take_query():

    # calling the Hello function for
    # maing it more interactive

    diagnostic_mode()
    # hello()
    # This loop is infinite as it will take
    # our queries continuously until and unless
    # we do not say bye to exit or terminate
    # the program
    while(True):

        # taking the query and making it into
        # lower case so that most of the times
        # query matches and we get the perfect
        # output

        query = take_command().lower()

        if "open google" in query:
            speak("Opening Google ")
            webbrowser.open("https://www.google.com/?client=safari")
            continue

        elif "what day is it" in query:
            tell_day()
            continue

        elif "what time is it" in query:
            tell_time()
            continue

        elif "from wikipedia" in query:

            speak(f" I am checking for{query}")
            query = query.replace("wikipedia", "")

            # it will give the summary of 4 lines from
            # wikipedia we can increase and decrease number of sentences
            result = wikipedia.summary(query, sentences=4)
            print(f"According to wikipedia {result}")
            speak(f"According to wikipedia {result}")

        elif " your name" in query:
            speak(f"I am {ASSISTANT}. Your deskstop Assistant")

        elif "news" in query:
            news()
        elif "weather" in query:
            weather()
        elif "joke" in query:
            speak(pyjokes.get_joke())
        elif "quote" in query:
            quote()
        elif "functions" in query:
            speak("I can do lots of things, I can tell you the news, what the weather is like, search a topic on wikipedia, or even just what day it is. Would you like to ask me one of those?")
            response = take_command()
            if response == "yes":
                speak("What would you like to hear about?")
                # This problem where I cannot give more than one query is why intents were important in that video
                # I think that you should set up some kind of struct with trigger phrases and their corresponding functions

            else:
                speak("Okay, well then here is an insightful and wise quote for you")
                quote()

        elif " daily briefing" in query:

            speak("Here is your daily briefing")
            tell_day()
            tell_time()
            weather()

        elif "diagnostic mode" in query:
            diagnostic_mode()

        # this will exit and terminate the program
        elif "bye" in query:
            speak(f"Goodbye {USER}!")
            exit()


def take_query_intents():
    done = False
    while not done:
        query = take_command().lower()
        for iterate_1 in intents["greeting"]:
            if query == iterate_1:
                hello()
                break
        for iterate_2 in intents["quote"]:
            if query == iterate_2:
                quote()
                break
        for iterate_3 in intents["briefing"]:
            if query == iterate_3:
                briefing()
                done = True
        for iterate_4 in intents["news"]:
            if query == iterate_4:
                news()
                break
        for iterate_5 in intents["time"]:
            if query == iterate_5:
                tell_time()
                break
        for iterate_6 in intents["date"]:
            if query == iterate_6:
                tell_day()
                break
        for iterate_7 in intents["weather"]:
            if query == iterate_7:
                weather()
                break
        for iterate_8 in intents["wikipedia"]:
            if query == iterate_8:
                wikipedia()
                break
        for iterate_9 in intents["name"]:
            if query == iterate_9:
                name()
                break
        for iterate_10 in intents["wolfram"]:
            if query == iterate_10:
                wolfram()
                break
        for iterate_11 in intents["done"]:
            if query == iterate_11:
                speak("Goodbye")
                done = True


if __name__ == '__main__':

    #execution in main
    # take_query()
    print("Say hello!")
    
    take_query_intents()
