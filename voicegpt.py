import sys
import math
import time
import speech_recognition as sr
import serial
from espeak import espeak
import openai
import pygame
from gtts import gTTS

pygame.mixer.init()
#model_to_use="text-davinci-003" # most capable
model_to_use="text-curie-001"
#model_to_use="text-babbage-001"
#model_to_use="text-ada-001" # lowest token cost
r = sr.Recognizer()
openai.api_key="YOUR_API_KEY_HERE"
def chatGPT(query):
	response = openai.Completion.create(
	model=model_to_use,
	prompt=query,
	temperature=0,
	max_tokens=1000
	)
	return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']

def main():
	print('LED is ON while button is pressed (Ctrl-C for exit).')
	while True:
		with sr.Microphone() as source:
			print("Say something!")
			audio=r.listen(source)
			print("Recognizing Now....")
			try:
				command=str(r.recognize_google (audio))
				print("Google Speech Recognition thinks you said " + command)
				query=command
				(res, usage) = chatGPT(query)
				print(res)
				tts=gTTS(text=res, lang='en')
				tts.save("good.mp3")
				pygame.mixer.music.load("good.mp3")
				pygame.mixer.music.play()
				espeak.synth(res)
			except sr.UnknownValueError:
				print("Google Speech Recognition could not understand audio")
			except sr.RequestError as e:
				print(f"Could not request results from Google Speech Recognition service; {e}")
if __name__ == '__main__':
	main()