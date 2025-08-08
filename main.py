import io
import IPython.display as ipd
import grpc
import numpy as np
import riva.client
import wave
import platform
import os

auth = riva.client.Auth(uri='localhost:50051')

riva_asr = riva.client.ASRService(auth)
riva_tts = riva.client.SpeechSynthesisService(auth)

path = "audio_samples/output_test.wav"

SAMPLE_RATE_HERTZ = 16000 
LANGUAGE_CODE = "en-US"
AUDIO_ENCODINGS = riva.client.AudioEncoding.LINEAR_PCM 

def transcribe_audio_with_asr(path: str):
    with io.open(path, 'rb') as fh:
        content = fh.read()
    ipd.Audio(path)

    # Set up an offline/batch recognition request
    config = riva.client.RecognitionConfig()
    config.encoding = AUDIO_ENCODINGS # Audio encoding can be detected from wav
    config.sample_rate_hertz = SAMPLE_RATE_HERTZ      # Sample rate can be detected from wav and resampled if needed
    config.language_code = LANGUAGE_CODE              # Language code of the audio clip
    config.max_alternatives = 1                       # How many top-N hypotheses to return
    config.enable_automatic_punctuation = True        # Add punctuation when end of VAD detected
    config.audio_channel_count = 1                    # Mono channel

    response = riva_asr.offline_recognize(content, config)

    asr_best_transcript = response.results[0].alternatives[0].transcript
    print("ASR Transcript:", asr_best_transcript)
    print("ASR Response:", response) #for debugging purposes
    return asr_best_transcript, response

def save_tts_audio_as_wav(audio_bytes, filename):
    sample_rate = 48000
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)          # Mono channel
        wf.setsampwidth(2)          # 16-bit audio (2 bytes per sample)
        wf.setframerate(sample_rate) # Sample rate (Hz)
        wf.writeframes(audio_bytes)
    print(f"Saved synthesized speech to {filename}")


def output_text_to_speech(asr_best_transcript: str):
    req = {
        "language_code": LANGUAGE_CODE,
        "encoding": AUDIO_ENCODINGS,
        "voice_name": "English-US.Female-1",
        "text": asr_best_transcript
    }

    resp = riva_tts.synthesize(**req)
    audio_samples = np.frombuffer(resp.audio, dtype=np.int16)
    ipd.Audio(audio_samples, rate=SAMPLE_RATE_HERTZ)
    print("TTS Response:", resp)  # for debugging purposes

    save_tts_audio_as_wav(resp.audio, "tts_output.wav")

asr_best_transcript, response = transcribe_audio_with_asr(path)

output_text_to_speech(asr_best_transcript)