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
    text = asr_client.transcribe("audio_samples/input_audio_ship.wav")

    #Get intent and slots from text
    pred_intents, pred_slots = nlu_client.predict_intent_slots(text)
    print(f"Intents: {pred_intents} Slots: {pred_slots}")

    answer = db_helper.query_database(pred_intents, pred_slots, tokens=text.split())
    print(f"DB Query Result: {answer}")

    # Convert text back to speech and save output WAV
    tts_client.synthesize_and_save(answer, "audio_samples/tts_output.wav")

    db_helper.close()

if __name__ == "__main__":
    main()
