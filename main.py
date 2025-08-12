from riva_client.asr_client import RivaASRClient
from riva_client.nlp_client import RivaNLUClient
from riva_client.tts_client import RivaTTSClient
from db.db_helper import SQLiteHelper

def main():
    asr_client = RivaASRClient()
    nlu_client = RivaNLUClient()
    tts_client = RivaTTSClient()
    db_helper = SQLiteHelper()

    # Transcribe speech to text
    text = asr_client.transcribe("audio_samples/output_test.wav")
    
    #Get intent and slots from text
    intent, slots = nlu_client.predict_intent_slots(text)
    print(f"Intent: {intent}, Slots: {slots}")

    answer = db_helper.query_database(intent, slots)
    print(f"DB Query Result: {answer}")

    # Convert text back to speech and save output WAV
    tts_client.synthesize_and_save(text, "audio_samples/tts_output.wav")

    db_helper.close()

if __name__ == "__main__":
    main()
