import sqlite3
import csv
import os

DATA_DIR = "data"   # adjust if your train/val/test are elsewhere
DB_PATH = "db/assistant.db"

def load_list(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def read_tsv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [(row["sentence"], int(row["label"])) for row in reader]

def read_slots(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [list(map(int, line.strip().split())) for line in f]

def setup_schema(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS containers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT,
        location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS ships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cargo_type TEXT,
        destination TEXT,
        ship_name TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipment_id TEXT,
        type TEXT,
        status TEXT,
        location TEXT
    )""")
    conn.commit()

def extract_entities(tokens, slot_tags, slot_labels):
    entities = {}
    current_entity, current_type = [], None
    for token, tag_idx in zip(tokens, slot_tags):
        tag = slot_labels[tag_idx]
        if tag.startswith("B-"):
            if current_entity:
                entities.setdefault(current_type, []).append(" ".join(current_entity))
            current_type = tag[2:]
            current_entity = [token]
        elif tag.startswith("I-") and current_type == tag[2:]:
            current_entity.append(token)
        else:
            if current_entity:
                entities.setdefault(current_type, []).append(" ".join(current_entity))
                current_entity, current_type = [], None
    if current_entity:
        entities.setdefault(current_type, []).append(" ".join(current_entity))
    return entities

def insert_into_db(conn, intent, entities):
    cur = conn.cursor()

    if intent in ["book_container", "update_container_destination", "check_container", "check_container_status"]:
        for name in entities.get("container_name", []):
            cur.execute("INSERT INTO containers (name, status, location) VALUES (?, ?, ?)",
                        (name, "Unknown", entities.get("location", ["Unknown"])[0] if "location" in entities else None))

    elif intent in ["list_containers", "list_containers_by_location"]:
        for loc in entities.get("location", []):
            cur.execute("INSERT INTO containers (name, status, location) VALUES (?, ?, ?)",
                        (f"Container_{loc}", "Unknown", loc))

    elif intent in ["query_ship_location", "query_ship_schedule"]:
        for ship in entities.get("ship_name", []):
            loc = entities.get("location", ["Unknown"])[0] if "location" in entities else "Unknown"
            cur.execute("INSERT INTO ships (name, location) VALUES (?, ?)", (ship, loc))

    elif intent in ["book_shipment", "cancel_shipment"]:
        cargo = entities.get("cargo_type", ["Unknown"])[0]
        dest = entities.get("location", ["Unknown"])[0]
        ship = entities.get("ship_name", ["Unknown"])[0]
        cur.execute("INSERT INTO shipments (cargo_type, destination, ship_name) VALUES (?, ?, ?)",
                    (cargo, dest, ship))

    elif intent in ["schedule_maintenance", "check_equipment_status", "cancel_equipment", "list_equipment_by_location"]:
        eid = entities.get("equipment_id", ["Unknown"])[0]
        etype = entities.get("equipment_type", ["Unknown"])[0] if "equipment_type" in entities else None
        loc = entities.get("location", ["Unknown"])[0] if "location" in entities else None
        cur.execute("INSERT INTO equipment (equipment_id, type, status, location) VALUES (?, ?, ?, ?)",
                    (eid, etype, "Unknown", loc))

    conn.commit()

def populate():
    intents = load_list(os.path.join(DATA_DIR, "dict.intents.csv"))
    slots = load_list(os.path.join(DATA_DIR, "dict.slots.csv"))

    datasets = [
        ("train.tsv", "train_slots.tsv"),
        ("val.tsv", "val_slots.tsv"),
        ("test.tsv", "test_slots.tsv"),
    ]

    conn = sqlite3.connect(DB_PATH)
    setup_schema(conn)

    for sent_file, slot_file in datasets:
        if not os.path.exists(os.path.join(DATA_DIR, sent_file)):
            continue
        sents = read_tsv(os.path.join(DATA_DIR, sent_file))
        slot_tags = read_slots(os.path.join(DATA_DIR, slot_file))

        for (sentence, intent_idx), slots_for_sent in zip(sents, slot_tags):
            intent = intents[intent_idx]
            tokens = sentence.split()
            entities = extract_entities(tokens, slots_for_sent, slots)
            insert_into_db(conn, intent, entities)

    conn.close()
    print(f"✅ Populated database at {DB_PATH}")

if __name__ == "__main__":
    populate()
