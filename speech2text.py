from pygame import mixer # Load the required library
import speech_recognition as sr
import datetime
import thread

recognizer = sr.Recognizer()
microphone = sr.Microphone()
mixer.init()
songs = ["1", "2", "3", "4"]

def switchmusic(i):
	mixer.music.load('music/' + songs[i] + '.mp3')
	mixer.music.play()

def recognize_speech_from_mic():
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

	try:
		response["transcription"] = recognizer.recognize_google(audio)
	except:
		pass

	return response 

def coolmusic():
	i = 0
	while True:
		voiceIn = recognize_speech_from_mic()
		results = voiceIn["transcription"]
		if(results != None):
			print("results " + results)
		else:
			print("none")

		now = datetime.datetime.now()
		if results == None or now.second == 5:
			print("say again")
		elif results.find('next') != -1:
			print("Playing next song:")
			i += 1
			i = i % len(songs)
			switchmusic(i)
		elif results.find('back') != -1:
			print("Playing previous song:")
			i -= 1
			i = i % len(songs)	
			switchmusic(i)
		elif results.find('good') != -1:
			print("")
			break
		else:
			print("Please repeat")

def startcoolmusic():
	thread.start_new_thread(coolmusic, ())

		