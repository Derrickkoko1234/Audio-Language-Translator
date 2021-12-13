import speech_recognition as sr
from google_trans_new import google_translator
# from googletrans import Translator
import pyttsx3

running = True

recognizer = sr.Recognizer()
engine = pyttsx3.init()

while running:
  with sr.Microphone() as source:
    print('Clearing background noises...')
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print('Waiting for your message')
    audio = recognizer.listen(source, timeout=20)
    print('Done recording')
  try:
    print('Recognizing...')
    result = recognizer.recognize_google(audio, language='en')
    print(result)
    if 'exit' or 'stop' or 'close' in result:
      engine.stop()
  except Exception as ex:
    print(ex)

  # Translation function
  def trans():
    langinput = input('Enter the language you want to translate: ')
    translator = google_translator()
    translate_text = translator.translate(str(result), lang_tgt=str(langinput))
    print(translate_text)
    engine.say(str(translate_text))
    engine.runAndWait()

  trans()

