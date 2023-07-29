import os
import pyaudio
import threading
from google.cloud import texttospeech, translate

# Set up Google Cloud credentials (replace 'YOUR_API_KEY' with your actual API key)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

# Initialize Text-to-Speech and Translation clients
text_to_speech_client = texttospeech.TextToSpeechClient()
translate_client = translate.TranslationServiceClient()

def translate_text(text, target_language):
    parent = f"projects/[YOUR_PROJECT_ID]"  # Replace with your Google Cloud project ID
    response = translate_client.translate_text(
        contents=[text],
        target_language_code=target_language,
        parent=parent
    )

    return response.translations[0].translated_text

def text_to_speech(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Source language (English)
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = text_to_speech_client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content

def translate_and_print(transcript, target_language):
    # Translate the text
    translated_text = translate_text(transcript, target_language)
    print("Translated:", translated_text)

    # Convert the translated text to speech and play it
    audio_data = text_to_speech(translated_text)
    play_audio(audio_data)

def play_audio(audio_data):
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        output=True
    )

    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    audio.terminate()

def audio_streaming():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Streaming audio and translating in real-time. Press Ctrl+C to stop.")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            # Here, you can process the audio data or use a speech-to-text API to convert it to text.
            # For simplicity, we'll directly pass the audio data as text to the translation function.
            translate_and_print(data, target_language="fr")  # Replace "fr" with your target language code

    except KeyboardInterrupt:
        print("Streaming stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

if __name__ == "__main__":
    audio_streaming()



# import speech_recognition as sr
# from google_trans_new import google_translator
# # from googletrans import Translator
# import pyttsx3

# running = True
# """
# The main loop for the program. This is where the program will run until the user tells the program to quit.
# @returns nothing
# """

# recognizer = sr.Recognizer()
# """
# Initialize the recognizer and engine for text to speech.
# """
# engine = pyttsx3.init()

# while running:
#   result = ''
#   with sr.Microphone() as source:
#     print('Clearing background noises...')
#     engine.say('Clearing background noises...')
#     recognizer.adjust_for_ambient_noise(source, duration=1)
#     print('Waiting for your message')
#     audio = recognizer.listen(source, timeout=20)
#     print('Done recording')
#   try:
#     print('Recognizing...')
#     result = recognizer.recognize_google(audio, language='en')
#     print(result)
#     if 'exit' or 'stop' or 'close' in result:
#       engine.stop()
#   except Exception as ex:
#     print(ex)

#   # Translation function
#   def trans():
#     langinput = input('Enter the language you want to translate: ')
#     translator = google_translator()
#     translate_text = translator.translate(str(result), lang_tgt=str(langinput))
#     print(translate_text)
#     engine.say(str(translate_text))
#     engine.runAndWait()

#   trans()


