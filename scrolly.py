import scrollphathd as scroll
from scrollphathd.fonts import font3x5
import time
import ha_api
import dotenv
import os

dotenv.load_dotenv()

UPDATE_TIME_SECONDS = int(os.getenv("UPDATE_TIME_SECONDS", "10"))
print(f"Update time: {UPDATE_TIME_SECONDS} seconds.")
BRIGHTNESS = float(os.getenv("BRIGHTNESS", "0.2"))
print(f"Brightness: {BRIGHTNESS}.")

def show_message(msg):
    scroll.clear()
    scroll.write_string(msg, x=1, y=1, brightness=BRIGHTNESS, font=font3x5)
    scroll.show()

def main():
    print("Initializing scrollphathd...")
    ha_api.send_status("starting", "Initializing scrollphathd LED display with pi Zero.")
    scroll.flip(x=True, y=True)

    while True:
        loop()
        print(f"Warte {UPDATE_TIME_SECONDS} Sekunden...")
        ha_api.send_status("waiting", f"Next update in {UPDATE_TIME_SECONDS} seconds.")
        time.sleep(UPDATE_TIME_SECONDS)

def loop():
    print("Getting sensor values...")
    ha_api.send_status("updating", f"Using entities {ha_api.ENTITY_ID_STROMVERBRAUCH} and {ha_api.ENTITY_ID_PV}")

    show_message("strm")
    time.sleep(2)
    val = ha_api.get_sensor_value(ha_api.ENTITY_ID_STROMVERBRAUCH)
    # check if val is a number
    try:
        float(val)
    except (TypeError, ValueError):
        print("! Abgerufener Wert ist keine Zahl.")
        show_message("Err")
        return

    strom = float(val)
    strom_k = round(strom / 1000, 1)
    print(f"Stromverbrauch: {strom_k} kW")

    show_message(str(strom_k))
    time.sleep(5)

    """""
    show_message("pv")
    time.sleep(2)
    val = ha_api.get_sensor_value(ha_api.ENTITY_ID_PV)
    if val is None:
        print("! Fehler beim Abrufen der PV-Leistung.")
        show_message("Err")
        return
    pv = float(val)
    pv_k = round(pv / 1000, 1)
    show_message(str(pv_k))
    time.sleep(5)
    """

if __name__ == "__main__":
    main()
    ha_api.send_status("stopped")
