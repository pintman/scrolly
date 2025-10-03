import requests
import dotenv
import os

dotenv.load_dotenv()

HASS_URL = os.getenv("HASS_URL", "http://homeassistant.local:8123")  # oder IP-Adresse
TOKEN = os.getenv("HASS_TOKEN")
ENTITY_ID_STROMVERBRAUCH = os.getenv("ENTITY_ID_STROMVERVERBRAUCH")
ENTITY_ID_PV = os.getenv("ENTITY_ID_PV")

HEADERS ={
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

if not TOKEN or not ENTITY_ID_STROMVERBRAUCH or not ENTITY_ID_PV:
    raise ValueError("Environment variables missing.")

def get_sensor_value(entity_id: str) -> str | None:
    "Fetch sensor value from Home Assistant for given entity_id."

    try:
        response = requests.get(f"{HASS_URL}/api/states/{entity_id}", 
                                headers=HEADERS, timeout=10)
    except requests.exceptions.RequestException as e:
        print("! Request failed:", e)
        return None

    if response.status_code == 200:
        data = response.json()
        value = data["state"]   # hier ist dein Wert als String
        return value
    else:
        print("! Fehler:", response.status_code, response.text)

def send_status(state: str="display updated", details: str="") -> None:
    "Send status update to Home Assistant."

    data = {
        "state": state,
        "attributes": {
            "friendly_name": "Scrolly",
            "icon": "mdi:robot", # from https://pictogrammers.com/library/mdi/
        }
    }
    if details:
        data["attributes"]["details"] = details

    try:
        response = requests.post(f"{HASS_URL}/api/states/sensor.scrolly", headers=HEADERS, json=data)
    except requests.exceptions.RequestException as e:
        print("! Request failed:", e)
        return


if __name__ == "__main__":
    v = get_sensor_value(ENTITY_ID_STROMVERBRAUCH)
    print("Wert Stromverbrauch:", v)
    v = get_sensor_value(ENTITY_ID_PV)
    print("Wert PV:", v)

    print("Sende Status...")
    send_status("testing", "Dies ist ein Test.")
    

