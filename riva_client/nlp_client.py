import riva.client
from riva.client.proto import riva_nlp_pb2 as rnlp
from nemo.collections.nlp.models import IntentSlotClassificationModel

class RivaNLUClient:
    def __init__(self, model_path="intent_slot_model.nemo", data_dir="./data/intent_slot", uri="localhost:50051"):
        self.auth = riva.client.Auth(uri=uri)
        self.nlp = riva.client.NLPService(self.auth)
        self.model = IntentSlotClassificationModel.restore_from(model_path)
        self.model.update_data_dir_for_testing(data_dir=data_dir)

    def predict_intent_slots(self, text: str):

        model = IntentSlotClassificationModel.restore_from("intent_slot_model.nemo")

        queries = [text]

        pred_intents, pred_slots = model.predict_from_examples(queries, self.model.cfg.test_ds)

        for query, intent, slots in zip(queries, pred_intents, pred_slots):
            print(f'Query : {query}')
            print(f'Predicted Intent: {intent}')
            print(f'Predicted Slots: {slots}')

        return pred_intents, pred_slots
"""
        response = self.nlp.analyze_intent(text)
        # Example response parsing (depends on exact Riva API version):
        intent = response.intent if hasattr(response, "intent") else None

        # Extract slots as a dict
        slots = {slot.slot_name: slot.slot_value for slot in response.slots} if hasattr(response, "slots") else {}

        return intent, slots
"""
