import pandas as pd
from sklearn.model_selection import train_test_split
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(project_root, "data")

sent_file = os.path.join(data_dir, "train.tsv")
slot_file = os.path.join(data_dir, "train_slots.tsv")

train_sent_out = os.path.join(data_dir, "train.tsv")
train_slot_out = os.path.join(data_dir, "train_slots.tsv")
val_sent_out = os.path.join(data_dir, "val.tsv")
val_slot_out = os.path.join(data_dir, "val_slots.tsv")
test_sent_out = os.path.join(data_dir, "test.tsv")
test_slot_out = os.path.join(data_dir, "test_slots.tsv")

# Read files
sentences = pd.read_csv(sent_file, sep="\t")   # sentence + intent
slots = pd.read_csv(slot_file, sep="\t", header=None)  # slots only

# Safety check: ensure same length
assert len(sentences) == len(slots), "Mismatch between sentences and slots length!"

# Merge temporarily to keep alignment
data = pd.concat([sentences, slots], axis=1)

# First split: train vs temp
train_data, temp_data = train_test_split(data, test_size=0.2, random_state=42, shuffle=True)

# Second split: val vs test (50/50 of temp → 10% each)
val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42, shuffle=True)

# Function to save splits back into separate files
def save_split(df, sent_path, slot_path):
    df.iloc[:, :2].to_csv(sent_path, sep="\t", index=False)   # sentence + label
    df.iloc[:, 2:].to_csv(slot_path, sep="\t", index=False, header=False)  # slots only

# Save
save_split(train_data, train_sent_out, train_slot_out)
save_split(val_data, val_sent_out, val_slot_out)
save_split(test_data, test_sent_out, test_slot_out)

# Print counts
print(f"Train: {len(train_data)} examples")
print(f"Val:   {len(val_data)} examples")
print(f"Test:  {len(test_data)} examples")
