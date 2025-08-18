from lightning.pytorch import Trainer
from omegaconf import DictConfig, OmegaConf

from nemo.collections.nlp.models import IntentSlotClassificationModel
from nemo.core.config import hydra_runner
from nemo.utils import logging
from nemo.utils.exp_manager import exp_manager

@hydra_runner(config_path="../configs", config_name="intent_slot_classification_config.yaml")

def main(cfg: DictConfig) -> None:
    # PTL 2.0 has find_unused_parameters as False by default, so its required to set it to True
    # when there are unused parameters like here
    #if cfg.trainer.strategy == 'ddp':
    #    cfg.trainer.strategy = "ddp_find_unused_parameters_true"
    logging.info(f'Config Params:\n {OmegaConf.to_yaml(cfg)}')
    trainer = Trainer(**cfg.trainer)
    exp_manager(trainer, cfg.get("exp_manager", None))

    # initialize the model using the config file
    model = IntentSlotClassificationModel(cfg.model, trainer=trainer)

    # training
    logging.info("================================================================================================")
    logging.info('Starting training...')
    trainer.fit(model)
    logging.info('Training finished!')

    # Stop further testing as fast_dev_run does not save checkpoints
    if trainer.fast_dev_run:
        return

    # after model training is done, you can load the model from the saved checkpoint
    # and evaluate it on a data file or on given queries.
    logging.info("================================================================================================")
    logging.info("Starting the testing of the trained model on test set...")
    logging.info("We will load the latest model saved checkpoint from the training...")

    # for evaluation and inference you can load the previously trained model saved in .nemo file
    # like this in your code, but we will just reuse the trained model here
    # eval_model = IntentSlotClassificationModel.restore_from(restore_path=checkpoint_path)
    eval_model = model

    # we will setup testing data reusing the same config (test section)
    eval_model.update_data_dir_for_testing(data_dir=cfg.model.data_dir)
    eval_model.setup_test_data(test_data_config=cfg.model.test_ds)

    trainer.test(model=eval_model, ckpt_path=None, verbose=False)
    logging.info("Testing finished!")

    # run an inference on a few examples
    logging.info("======================================================================================")
    logging.info("Evaluate the model on the given queries...")

    # this will work well if you train the model on Assistant dataset
    # for your own dataset change the examples appropriately
    queries = [
        'Update container Z',
        'Book shipment of steel beams',
        'Check container X for 16th August',
    ]

    pred_intents, pred_slots = eval_model.predict_from_examples(queries, cfg.model.test_ds)

    logging.info('The prediction results of some sample queries with the trained model:')
    for query, intent, slots in zip(queries, pred_intents, pred_slots):
        logging.info(f'Query : {query}')
        logging.info(f'Predicted Intent: {intent}')
        logging.info(f'Predicted Slots: {slots}')

    logging.info("Inference finished!")

    # Save the trained model to a .nemo archive
    logging.info("Saving the trained model to .nemo archive...")
    model.save_to(cfg.model.nemo_path)
    logging.info(f"Model saved to: {cfg.model.nemo_path}")

if __name__ == '__main__':
    main()
