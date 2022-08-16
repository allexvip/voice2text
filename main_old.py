from pydub import AudioSegment
import os


def mp3_to_wav(source, skip=0, excerpt=False):
    sound = AudioSegment.from_mp3(source)  # load source
    sound = sound.set_channels(1)  # mono
    sound = sound.set_frame_rate(16000)  # 16000Hz

    if excerpt:
        excrept = sound[skip * 1000:skip * 1000 + 30000]  # 30 seconds - Does not work anymore when using skip
        output_path = os.path.splitext(source)[0] + "_excerpt.wav"
        excrept.export(output_path, format="wav")
    else:
        audio = sound[skip * 1000:]
        output_path = os.path.splitext(source)[0] + ".wav"
        audio.export(output_path, format="wav")

    return output_path

print(os.getcwd()+r'\test.mp3') #"C:\Users\Alex\PycharmProjects\voice2text\test.mp3"
mp3_to_wav(os.getcwd()+r'\test.mp3',37,True)


#-------------------
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel
# open audio file
wf = wave.open('test.wav', "rb")

# Initialize model
# You can find several models at https://alphacephei.com/vosk/models
# I decided to go with the largest vosk-model-en-us-0.22
model = Model("/model")
rec = KaldiRecognizer(model, wf.getframerate())

#--------
import json

# To store our results
transcription = []

#rec.SetWords(True)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        # Convert json output to dict
        result_dict = json.loads(rec.Result())
        # Extract text values and append them to transcription list
        transcription.append(result_dict.get("text", ""))

# Get final bits of audio and flush the pipeline
final_result = json.loads(rec.FinalResult())
transcription.append(final_result.get("text", ""))

# merge or join all list elements to one big string
transcription_text = ' '.join(transcription)
print(transcription_text)


