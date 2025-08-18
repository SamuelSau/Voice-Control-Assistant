import pandas as pd

# ---- Check intents ----
for split in ["train", "val", "test"]:
    df = pd.read_csv(f"./data/{split}.tsv", sep="\t", header=0)  # since you said there is a header
    bad = df[["label"]][(df["label"] < 0) | (df["label"] > 14)]
    if not bad.empty:
        print(f"{split}.tsv has invalid intents:", bad["label"].unique())

# ---- Check slots ----
for split in ["train", "val", "test"]:
    with open(f"./data/{split}_slots.tsv") as f:
        for i, line in enumerate(f, 1):
            slots = [int(x) for x in line.strip().split()]
            bad = [s for s in slots if s < 0 or s > 14]
            if bad:
                print(f"{split}_slots.tsv line {i} has invalid slot IDs: {bad}")
