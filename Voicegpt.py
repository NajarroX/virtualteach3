import openai
import pyttsx3
import speech_recognition as sr
import time
from gtts import gTTS
import pyglet
import os

# OpenAI Api key
openai.api_key = "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"

# inicializar el text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error..")

def generate_response(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 2000,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    #voice_id = 'spanish-latin-am'
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # wait for user to say genius
        print("Di 'Teacher' para empezar a preguntar..")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio, language="es-GT")
                if transcription.lower() == "teacher":
                    #record audio
                    filename = "input.wav"
                    print("Cual es tu pregunta...")
                    #saludo = "pregunta.mp3"
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit = None, timeout = None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    # transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"Tu pregunta es: {text}")
                        # Generate response using ChatGPT-3
                        response = generate_response(text)
                        print(f"El Profesor Dice: {response}")
                        # record audio with gtts for video
                        tts = gTTS(text = response, lang ='es')
                        tts.save("sample.mp3")
                        # Read response using text - to speech
                        music = pyglet.resource.media('sample.mp3')
                        music.play()
                        os.remove('sample.mp3')
                        #pyglet.app.run()
                        #pyglet.app.exit()
                        #speak_text(response)
                        
                           
            except Exception as e:
                print("An error ocurred: {}".format(e))
if __name__ == "__main__":
    main()
    