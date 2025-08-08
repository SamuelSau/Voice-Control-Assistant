#!/bin/bash

if ! command -v ngc &> /dev/null; then
  echo "NGC CLI not found. Please install from: https://ngc.nvidia.com/setup"
  exit 1
fi

ngc config set

mkdir -p ../models

echo "Downloading ASR model: Conformer CTC Large"
ngc registry model download-version "nvidia/riva/speechtotext_en_us_conformer_ctc_large:deployable_v4.0" \
  --dest ../models

echo "Downloading NLP model: Joint Intent Slot BERT"
ngc registry model download-version "nvidia/riva/nlp_intent_slot_en_bert:deployable_v1.0" \
  --dest ../models

echo "Downloading TTS model: FastPitch + HiFiGAN"
ngc registry model download-version "nvidia/tao/speechsynthesis_english_fastpitch:deployable_v1.1" \
  --dest ../models

echo "Download complete. You should now have .riva and/or .rmir files in the models folder."