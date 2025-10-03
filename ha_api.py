import requests
import dotenv
import os

dotenv.load_dotenv()

HASS_URL = os.getenv("HASS_URL", "http://homeassistant.local:8123")  # oder IP-Adresse
TOKEN = os.getenv("HASS_TOKEN")
ENTITY_ID_STROMVERBRAUCH = os.getenv("ENTITY_ID_STROMVERVERBRAUCH")
ENTITY_ID_PV = os.getenv("ENTITY_ID_PV")

if not TOKEN or not ENTITY_ID_STROMVERBRAUCH or not ENTITY_ID_PV:
    raise ValueError("Environment variables missing.")

def get_sensor_value(entity_id):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(f"{HASS_URL}/api/states/{entity_id}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        value = data["state"]   # hier ist dein Wert als String
        return value
    else:
        print("Fehler:", response.status_code, response.text)

if __name__ == "__main__":
    v = get_sensor_value(ENTITY_ID_STROMVERBRAUCH)
    print("Wert Stromverbrauch:", v)
    v = get_sensor_value(ENTITY_ID_PV)
    print("Wert PV:", v)

