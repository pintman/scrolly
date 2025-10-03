import requests
import dotenv
import os

dotenv.load_dotenv()

HASS_URL = os.getenv("HASS_URL", "http://homeassistant.local:8123")  # oder IP-Adresse
TOKEN = os.getenv("HASS_TOKEN")
ENTITY_ID = os.getenv("ENTITY_ID")

if not TOKEN or not ENTITY_ID:
    raise ValueError("HASS_TOKEN und ENTITY_ID müssen gesetzt sein.")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

response = requests.get(f"{HASS_URL}/api/states/{ENTITY_ID}", headers=headers)

if response.status_code == 200:
    data = response.json()
    value = data["state"]   # hier ist dein Wert als String
    print(f"Sensorwert: {ENTITY_ID}", value)
else:
    print("Fehler:", response.status_code, response.text)
