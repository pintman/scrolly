import scrollphathd as scroll
from scrollphathd.fonts import font3x5
import time
import ha_api
      

def show_message(msg):
    scroll.clear()
    scroll.write_string(msg, brightness=0.5, font=font3x5)
    scroll.show()

def main():
    print("Initializing scrollphathd...")
    scroll.flip(x=True, y=True)

    print("Getting sensor values...")

    show_message("strm")
    time.sleep(2)
    strom = float(ha_api.get_sensor_value(ha_api.ENTITY_ID_STROMVERBRAUCH))
    strom_k = round(strom / 1000, 1)
    show_message(str(strom_k))
    time.sleep(5)

    show_message("pv")
    time.sleep(2)
    pv = float(ha_api.get_sensor_value(ha_api.ENTITY_ID_PV))
    pv_k = round(pv / 1000, 1)
    show_message(str(pv_k))
    time.sleep(5)


if __name__ == "__main__":
    main()