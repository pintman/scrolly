import scrollphathd as scroll
from scrollphathd.fonts import font3x5
import time
import ha_api
import dotenv

dotenv.load_dotenv()

UPDATE_TIME_SECONDS = int(dotenv.get_key(dotenv.find_dotenv(), "UPDATE_TIME_SECONDS"))
BRIGHTNESS = float(dotenv.get_key(dotenv.find_dotenv(), "BRIGHTNESS", "0.2"))

def show_message(msg):
    scroll.clear()
    scroll.write_string(msg, brightness=BRIGHTNESS, font=font3x5)
    scroll.show()

def main():
    print("Initializing scrollphathd...")
    scroll.flip(x=True, y=True)

    while True:
        loop()
        print(f"Warte {UPDATE_TIME_SECONDS} Sekunden...")
        time.sleep(UPDATE_TIME_SECONDS)

def loop():
    print("Getting sensor values...")

    show_message("strm")
    time.sleep(2)
    val = ha_api.get_sensor_value(ha_api.ENTITY_ID_STROMVERBRAUCH)
    if val is None:
        print("! Fehler beim Abrufen des Stromverbrauchs.")
        show_message("Err")
        return    
    strom = float(val)
    strom_k = round(strom / 1000, 1)
    show_message(str(strom_k))
    time.sleep(5)

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


if __name__ == "__main__":
    main()