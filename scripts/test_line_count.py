for split in ["train", "val", "test"]:
    with open(f"../data/{split}.tsv") as f_sent, open(f"../data/{split}_slots.tsv") as f_slot:
        num_sents = sum(1 for _ in f_sent) - 1  # minus header
        num_slots = sum(1 for _ in f_slot)
        print(f"{split}: {num_sents} sentences, {num_slots} slot lines")
