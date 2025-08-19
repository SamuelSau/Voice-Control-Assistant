import sqlite3
from typing import Dict, Any, List

class SQLiteHelper:
    def __init__(self, db_path="db/assistant.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def parse_slots(self, tokens: List[str], tags: List[str]) -> Dict[str, str]:
        """
        Convert BIO slot tags into a dictionary of slot_name -> value.
        Example:
            tokens = ["Book", "shipment", "to", "Tokyo"]
            tags   = ["O", "O", "O", "B-location"]
            => {"location": "Tokyo"}
        """
        slots = {}
        current_slot = None
        current_tokens = []

        for token, tag in zip(tokens, tags):
            if tag == "O":
                if current_slot:
                    slots[current_slot] = " ".join(current_tokens)
                    current_slot, current_tokens = None, []
                continue

            prefix, slot_type = tag.split("-", 1)

            if prefix == "B":
                if current_slot:
                    slots[current_slot] = " ".join(current_tokens)
                current_slot = slot_type
                current_tokens = [token]

            elif prefix == "I" and current_slot == slot_type:
                current_tokens.append(token)
            else:
                # If mismatch, reset
                if current_slot:
                    slots[current_slot] = " ".join(current_tokens)
                current_slot = slot_type
                current_tokens = [token]

        if current_slot:
            slots[current_slot] = " ".join(current_tokens)

        return slots


    def query_database(self, intent_list: List[str], slots_list: List[str], tokens: List[str]):
        """
        intent_list: ['query_ship_location']
        slots_list:  ['O O B-ship_name I-ship_name B-location']
        tokens:     ['Where', 'is', 'ship', 'Evergreen', 'Tokyo']
        """
        intent = intent_list[0] if intent_list else None
        slot_tags = slots_list[0].split() if slots_list else []
        slot_values = self.parse_slots(tokens, slot_tags)

        cursor = self.conn.cursor()

        # Intent-to-query mapping
        if intent == "query_ship_location":
            ship_name = slot_values.get("ship_name")
            cursor.execute("SELECT location FROM ships WHERE name=?", (ship_name,))
            result = cursor.fetchone()
            return result["location"] if result else f"Location unknown for ship {ship_name}"

        elif intent == "check_container":
            container_name = slot_values.get("container_name")
            cursor.execute("SELECT status FROM containers WHERE name=?", (container_name,))
            result = cursor.fetchone()
            return result["status"] if result else f"Unknown container {container_name}"

        elif intent == "check_container":
            container_name = slot_values.get("container_name")
            cursor.execute("SELECT status FROM containers WHERE name=?", (container_name,))
            result = cursor.fetchone()
            return result["status"] if result else "Unknown container"

        elif intent == "list_containers":
            cursor.execute("SELECT name FROM containers")
            return [row["name"] for row in cursor.fetchall()]

        elif intent == "check_container_status":
            container_name = slot_values.get("container_name")
            cursor.execute("SELECT status FROM containers WHERE name=?",(container_name,))
            result = cursor.fetchone()
            return result["status"] if result else "Unknown container"

        elif intent == "list_containers_by_location":
            location = slot_values.get("location")
            cursor.execute("SELECT name FROM containers WHERE location=?",(location,))
            return [row["name"] for row in cursor.fetchall()]

        elif intent == "schedule_maintenance":
            equipment_id = slot_values.get("equipment_id")
            date = slot_values.get("date")
            cursor.execute("INSERT INTO maintenance_schedule (equipment_id, date) VALUES (?, ?)",(equipment_id, date))
            self.conn.commit()
            return f"Maintenance for {equipment_id} scheduled on {date}."

        elif intent == "query_ship_schedule":
            ship_name = slot_values.get("ship_name")
            cursor.execute("SELECT schedule FROM ships WHERE name=?",(ship_name,))
            result = cursor.fetchone()
            return result["schedule"] if result else "Unknown ship"

        elif intent == "query_ship_location":
            print("Debug: Entered query_ship_location intent")
            ship_name = slot_values.get("ship_name")
            cursor.execute("SELECT location FROM ships WHERE name=?",(ship_name,))
            result = cursor.fetchone()
            return result["location"] if result else "Unknown ship location"

        elif intent == "update_container_destination":
            container_name = slot_values.get("container_name")
            location = slot_values.get("location")
            cursor.execute("UPDATE containers SET location=? WHERE name=?",(location, container_name))
            self.conn.commit()
            return f"Container {container_name} destination updated to {location}."

        elif intent == "check_equipment_status":
            equipment_id = slot_values.get("equipment_id")
            cursor.execute("SELECT status FROM equipment WHERE id=?",(equipment_id,))
            result = cursor.fetchone()
            return result["status"] if result else "Unknown equipment"

        elif intent == "book_shipment":
            cargo_type = slot_values.get("cargo_type")
            date = slot_values.get("date")
            cursor.execute("INSERT INTO shipments (cargo_type, date) VALUES (?, ?)",(cargo_type, date))
            self.conn.commit()
            return f"Shipment of {cargo_type} booked on {date}."

        elif intent == "cancel_shipment":
            cargo_type = slot_values.get("cargo_type")
            cursor.execute("DELETE FROM shipments WHERE cargo_type=?",(cargo_type,))
            self.conn.commit()
            return f"Shipment of {cargo_type} cancelled."

        elif intent == "cancel_equipment":
            equipment_id = slot_values.get("equipment_id")
            cursor.execute("DELETE FROM equipment WHERE id=?",(equipment_id,))
            self.conn.commit()
            return f"Equipment {equipment_id} cancelled."

        elif intent == "list_equipment_by_location":
            location = slot_values.get("location")
            cursor.execute("SELECT id FROM equipment WHERE location=?",(location,))
            return [row["id"] for row in cursor.fetchall()]

        else:
            return "Intent not handled."

    def close(self):
        self.conn.close()
