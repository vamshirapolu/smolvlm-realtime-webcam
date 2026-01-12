import whisper

import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


model = whisper.load_model("base")
result = model.transcribe("/Users/vamshi/Downloads/335_Richard_Ave_Apt_C4.wav")
print(result["text"])