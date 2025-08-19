import riva.client
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

        return pred_intents, pred_slots
