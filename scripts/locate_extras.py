with open("../data/train.tsv") as f_sent, open("../data/train_slots.tsv") as f_slot:
    next(f_sent)  # skip header
    for idx, (sent_line, slot_line) in enumerate(zip(f_sent, f_slot), 1):
        sent_text = sent_line.strip().split("\t")[0]
        slots = slot_line.strip().split()
        tokens = sent_text.split()
        if len(tokens) != len(slots):
            print(f"Mismatch at train line {idx}:")
            print(f"  sentence: {sent_text}")
            print(f"  slots: {slot_line.strip()}")
    
    # Check if there are extra slot lines after running out of sentences
    remaining_slots = list(f_slot)
    if remaining_slots:
        print(f"Extra slot lines ({len(remaining_slots)}):")
        for line in remaining_slots:
            print(line.strip())
