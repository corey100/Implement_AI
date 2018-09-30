# import random
import datetime


import speech_recognition as sr

def main():
	recognizer = sr.Recognizer()
	microphone = sr.Microphone()
	print("talk...")
    # guess = recognize_speech_from_mic(recognizer, microphone)
	
	songs = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
	movies = ["ford", "chevy", "cadi", "bmw", "mercedes", "hyundai", "mazda"]
	loop = True
	while loop:
		i = 0
		while i < len(presidents):

			print(presidents[i])
			#ectra list
			print("hello")
			voiceIn = recognize_speech_from_mic(recognizer, microphone)
			#print(voiceIn["transcription"])
			results = voiceIn["transcription"]
			print(results)
			now = datetime.datetime.now()
			if results == None or now.second == 5:
				print("say again")
			elif results.find('next') != -1:
				print("Playing next song:")
				i += 1
			elif results.find('back') != -1:
				print("Playing previous song:")
				i -= 1	
			elif results.find('good') != -1:
				print("")
				break
			else:
				print("Please repeat")
		break		

		i = 0
		while i < len(cars):

			print(cars[i])
			print("Please choose ")
			voiceIn = recognize_speech_from_mic(recognizer, microphone)
			#print(voiceIn["transcription"])
			results = voiceIn["transcription"]
			print(results)
			now = datetime.datetime.now()
			if results == None or now.second == 5:
				print("say again")
			elif results.find('next') != -1:
				print("Playing next movie:")
				i += 1
			elif results.find('back') != -1:
				print("Playing previous movie:")
				i -= 1	
			elif results.find('good') != -1:
				print("goodbye")
				break
			else:
				print("Please repeat")
		break		

	

def recognize_speech_from_mic(recognizer, microphone):
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

    
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response 


if __name__ == "__main__":
	main()
 