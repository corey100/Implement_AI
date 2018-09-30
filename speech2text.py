# import random
import datetime
from threading import Thread
from pygame import mixer # Load the required library
import speech_recognition as sr

def main():
	mymy = musicplayer().start()
	
class musicplayer:

	def __init__(self, src=0):
		self.songs = ["sample", "haha"]
		# initialize the video camera stream and read the first frame
		# from the stream
		mixer.init()
		mixer.music.load('muic/sample.mp3')
		mixer.music.play()

		# init reco 
		self.recognizer = sr.Recognizer()
		self.microphone = sr.Microphone()
	
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	
	def recognize_speech_from_mic(self, recognizer, microphone):
		"""Transcribe speech from recorded from `microphone`.

		"Transcription": `None` if speech could not be transcribed,
				otherwise a string containing the transcribed text
		"""
		# check that recognizer and microphone arguments are appropriate type
		if not isinstance(recognizer, sr.Recognizer):
			raise TypeError("`recognizer` must be `Recognizer` instance")

		if not isinstance(microphone, sr.Microphone):
			raise TypeError("`microphone` must be `Microphone` instance")

		# adjust the recognizer sensitivity to ambient noise and record audio
		# from the microphone
		with microphone as source:
			recognizer.adjust_for_ambient_noise(source)
			audio = recognizer.listen(source)

		# set up the response object
		response = {
			"success": True,
			"error": None,
			"transcription": None
		}
		return response 

	def switchmusic(self, index):
		mixer.music.stop()
		mixer.music.load('muic/' + self.songs[index] + '.mp3')
		mixer.music.play()

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		i = 0
		while not self.stopped:
			voiceIn = recognize_speech_from_mic(self.recognizer, self.microphone)
			results = voiceIn["transcription"]
			now = datetime.datetime.now()
			if results == None or now.second == 5:
				print("say again")
			elif results.find('next') != -1:
				print("Playing next song:")
				i += 1
				i = i % len(self.songs)
				self.switchmusic(i)
			elif results.find('back') != -1:
				print("Playing previous song:")
				i -= 1
				i = i % len(self.songs)	
				self.switchmusic(i)
			elif results.find('good') != -1:
				print("")
				self.stopped = True
				break
			else:
				print("Please repeat")

if __name__ == "__main__":
	main()
 