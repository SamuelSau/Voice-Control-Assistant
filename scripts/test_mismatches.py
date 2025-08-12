for split in ["train", "val", "test"]:
    with open(f"../data/{split}.tsv") as f_sent, open(f"../data/{split}_slots.tsv") as f_slot:
        next(f_sent)  # skip header in sentences file
        for idx, (sent_line, slot_line) in enumerate(zip(f_sent, f_slot), 1):
            sent_text = sent_line.strip().split("\t")[0]
            tokens = sent_text.split()
            slots = slot_line.strip().split()
            if len(tokens) != len(slots):
                print(f"{split} line {idx} mismatch: {len(tokens)} tokens vs {len(slots)} slots")
