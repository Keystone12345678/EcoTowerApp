import json
import time
import os

SAVE_FILE = "savegame.json"

# Upgrade-Daten (yield-Werte angepasst an main.py)
UPGRADES_DATA = [
    {"name": "Moos-Teppich", "base_cost": 15, "yield": 0.5},
    {"name": "Algen-Behälter", "base_cost": 100, "yield": 2.0},
    {"name": "Solar-Fenster", "base_cost": 500, "yield": 8.0},
    {"name": "Wind-Ventilator", "base_cost": 1200, "yield": 25.0},
    {"name": "Büro-Botaniker", "base_cost": 3500, "yield": 70.0},
    {"name": "Regen-Turbine", "base_cost": 9000, "yield": 150.0},
    {"name": "Bio-Reaktor", "base_cost": 25000, "yield": 300.0},
    {"name": "CO2-Sauger", "base_cost": 75000, "yield": 600.0},
    {"name": "Quanten-Photo", "base_cost": 200000, "yield": 1500.0},
    {"name": "Fusion-Zelle", "base_cost": 500000, "yield": 3500.0}
]

def get_cost(base_cost, count):
    """Berechnet die Kosten basierend auf der Anzahl gekaufter Upgrades"""
    return int(base_cost * (1.15 ** count))

def save_game(energy, counts, certificates):
    """Speichert den aktuellen Spielstand"""
    data = {
        "energy": energy,
        "counts": counts,
        "certificates": certificates,
        "last_seen": time.time()
    }
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")
        return False

def load_game():
    """Lädt den Spielstand und berechnet Offline-Gewinn"""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                certs = data.get("certificates", 0)
                last_seen = data.get("last_seen", time.time())
                
                # Bonus berechnen (10% pro Zertifikat)
                bonus_mult = 1 + (certs * 0.1)
                
                # EPS für Offline-Gewinn berechnen
                eps = sum(data["counts"][i] * UPGRADES_DATA[i]["yield"] 
                         for i in range(min(len(data["counts"]), len(UPGRADES_DATA))))
                
                offline_time = time.time() - last_seen
                offline_gain = int(offline_time * eps * bonus_mult)
                
                data["energy"] += offline_gain
                
                # Sicherstellen, dass counts die richtige Länge hat
                while len(data["counts"]) < len(UPGRADES_DATA):
                    data["counts"].append(0)
                
                return data, offline_gain
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
    
    # Neues Spiel
    return {"energy": 0, "counts": [0] * len(UPGRADES_DATA), "certificates": 0}, 0
