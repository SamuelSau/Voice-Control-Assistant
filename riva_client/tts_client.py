import numpy as np
import riva.client
import wave

class RivaTTSClient:
    def __init__(self, uri="localhost:50051", sample_rate=48000, language_code="en-US", voice_name="English-US.Female-1"):
        self.auth = riva.client.Auth(uri=uri)
        self.tts = riva.client.SpeechSynthesisService(self.auth)
        self.sample_rate = sample_rate
        self.language_code = language_code
        self.voice_name = voice_name
    
    def synthesize(self, text: str) -> bytes:
        req = {
            "language_code": self.language_code,
            "encoding": riva.client.AudioEncoding.LINEAR_PCM,
            "voice_name": self.voice_name,
            "text": text
        }
        response = self.tts.synthesize(**req)
        print("TTS Response received")
        return response.audio
    
    def save_wav(self, audio_bytes: bytes, filename: str):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit PCM = 2 bytes per sample
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_bytes)
        print(f"TTS audio saved as {filename}")
    
    def synthesize_and_save(self, text: str, filename: str):
        audio_bytes = self.synthesize(text)
        self.save_wav(audio_bytes, filename)
