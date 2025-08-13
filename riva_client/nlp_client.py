import riva.client
from riva.client.proto import riva_nlp_pb2 as rnlp

class RivaNLUClient:
    def __init__(self, uri="localhost:50051"):
        self.auth = riva.client.Auth(uri=uri)
        self.nlp = riva.client.NLPService(self.auth)
    
    def predict_intent_slots(self, text: str):
        
        response = self.nlp.analyze_intent(text)
        # Example response parsing (depends on exact Riva API version):
        intent = response.intent if hasattr(response, "intent") else None

        # Extract slots as a dict
        slots = {slot.slot_name: slot.slot_value for slot in response.slots} if hasattr(response, "slots") else {}

        return intent, slots
