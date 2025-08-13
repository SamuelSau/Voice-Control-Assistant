import io
import riva.client
import numpy as np

class RivaASRClient:
    def __init__(self, uri="localhost:50051", sample_rate=16000, language_code="en-US"):
        self.auth = riva.client.Auth(uri=uri)
        self.asr = riva.client.ASRService(self.auth)
        self.sample_rate = sample_rate
        self.language_code = language_code
    
    def transcribe(self, audio_path: str) -> str:
        with io.open(audio_path, 'rb') as fh:
            content = fh.read()
        
        config = riva.client.RecognitionConfig()
        config.encoding = riva.client.AudioEncoding.LINEAR_PCM
        config.sample_rate_hertz = self.sample_rate
        config.language_code = self.language_code
        config.max_alternatives = 1
        config.enable_automatic_punctuation = True
        config.audio_channel_count = 1
        
        response = self.asr.offline_recognize(content, config)
        
        transcript = response.results[0].alternatives[0].transcript
        print(f"ASR Transcript: {transcript}")
        return transcript
