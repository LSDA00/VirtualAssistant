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

import json
import pickle
import numpy as np
import random

import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')



USER = "Lucas"
ASSISTANT= ", 8 oh 5"



def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def take_command():

    r = sr.Recognizer()
    query = " "
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            r.adjust_for_ambient_noise(source)
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
    # [1]=female voice in set Property. 7, 11, 17, 28, 33 are good
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
    random_greeting = random.randint(1,3)
    if(random_greeting == 1):
        hour = datetime.datetime.now().hour
        if(hour >= 0) and (hour < 12):
            speak(f"Good Morning {USER}, how can I help you?")
        elif(hour >= 12) and (hour < 18):
            speak(f"Good afternoon {USER}, how can I help you?")
        elif(hour >= 18) and (hour <= 24):
            speak(f"Good Evening {USER}, how can I help you?")
    if(random_greeting == 2):
    
        speak(f"Hey there {USER}, what can I do for you?")
    
    if(random_greeting == 3):
    
        speak(f"Hi {USER}, what's up?")
    


def wiki():
    speak("What would you like information about?")
    my_query = take_command().lower()
    speak(f" I am searching for {my_query}")
    my_query = my_query.replace("wikipedia", "")

    # it will give the summary of 4 lines from
    # wikipedia we can increase and decrease number of sentences
    result = wikipedia.summary(my_query, sentences=4)
    print(f"According to wikipedia {result}")
    speak(f"According to wikipedia {result}")


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
    # making it more interactive
    hello()
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
        ints = predict_class(query)
        #print(ints)
        tag = ints[0]['intent']
        #print(tag)
        res = get_response(ints, intents)

        if tag == 'google':
            speak(res)
            webbrowser.open("https://www.google.com/?client=safari")
            continue

        elif tag == 'date':
            tell_day()
            continue

        elif tag == 'time':
            tell_time()
            continue

        elif tag == 'wikipedia':
            speak(res)
            wiki()

        elif tag == 'name': 
            speak(res)
           

        elif tag == 'news':
            speak(res)
            news()
        elif tag == 'weather':
            speak(res)
            weather()
        elif tag == 'joke':
            speak(res)
            speak(pyjokes.get_joke())
        elif tag == 'quote':
            speak(res)
            quote()
        elif tag == 'briefing':
            speak(res)
            briefing()
        # this will exit and terminate the program
        elif tag == 'goodbye':
            speak(res)
            exit()
        elif tag == 'wolfram':
            wolfram()
        else: 
            speak("I'm sorry, something went wrong. Please try again")
            exit()


def main():

    print("Say hello!")
    take_query()
main()


 