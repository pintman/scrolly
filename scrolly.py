import scrollphathd as scroll
from scrollphathd.fonts import font5x7, font3x5
import time
import subprocess
import threading
import configparser
import ha_api

class Scrolly:
    """Scrolly waits for commands recevied as mqtt messages.

    It will act upon messages sent to the topic scrolly/# - the
    hashtag marks all subtopics.

    Topics
    ======
    
    scrolly/write: The payload will be written to the screen.

    scrolly/write_scroll: The payload will scroll over the
    screen. Scrolling continues until a new event occurs.

    scrolly/power: If the payload is 0, scrolly will be shutdown. A
    value of 1 is ignored.

    scrolly/brightness: A value between 0.0 and 1.0 sets the
    brightness level of the display.

    scrolly/status: 'online' or 'offline' depending of the status of scrolly.

    """
    
    def __init__(self, host="localhost"):
        self.subscribed_topic2method = {
            "scrolly/write_scroll": self.write_scroll,
            "scrolly/write": self.write,
            "scrolly/power": self.power,
            "scrolly/brightness": self.set_brightness}
        
        scroll.flip(x=True, y=True)
        scroll.set_brightness(0.2)
        scroll.clear()
        scroll.write_string("on")
        scroll.show()

        status_topic = "scrolly/status"
        self.mos = mosquitto.Mosquitto()
        self.mos.will_set(status_topic, "offline")
        self.mos.on_message = self.on_message
        self.debug("connecting to " + host)
        self.mos.connect(host)
        self.mos.publish("scrolly/power", 1)
        self.mos.publish(status_topic, "online")
        self.mos.subscribe("scrolly/#")

        self.stop_event = threading.Event()

        # start thread that is waiting for action in bluedot app
        th = threading.Thread(target=self._shutdown_on_bluedot_press_waiter)
        th.start()
        
        self.mos.loop_forever()

    def on_message(self, _msq, _userdata, msg):
        print("msg received", msg.topic, msg.payload)

        if msg.topic in self.subscribed_topic2method:
            self.stop_event.set()
            meth = self.subscribed_topic2method[msg.topic]
            meth(str(msg.payload, encoding="UTF8"))            

    def write_scroll(self, message, wait=0.08):
        scroll.clear()
        scroll.write_string(message, x=0, y=0, font=font5x7)

        self.stop_event.clear()
        th = threading.Thread(target=self._write_scroll_worker,
                              args=(wait,))
        th.start()

    def write(self, message):
        scroll.clear()
        scroll.write_string(message)
        scroll.show()

    def _write_scroll_worker(self, wait_time):
        """Method for the worker thread. It is running until the stop event
        occurs."""
        
        while not self.stop_event.is_set():
            scroll.scroll()
            scroll.show()
            time.sleep(wait_time)

    def set_brightness(self, brightness):        
        scroll.set_brightness(float(brightness))
        scroll.show()
            
    def power(self, on_off):
        if on_off == "0":
            self._shutdown()

    def _shutdown_on_bluedot_press_waiter(self):
        bd = bluedot.BlueDot()
        bd.wait_for_press()
        self._shutdown()

    def _shutdown(self):
        self.write("off")
        subprocess.call("sudo shutdown now", shell=True)

    def debug(self, msg):
        self.mos.publish("scrolly/debug", msg)
        

def show_message(msg):
    scroll.clear()
    scroll.flip(y=True)
    scroll.write_string(msg, brightness=0.5, font=font3x5)
    scroll.show()

def main():
    #config = configparser.ConfigParser()
    #config.read("scrolly.ini")
    #host = config["mqtt"]["host"]
    #Scrolly(host)

    print("Getting sensor values...")
    strom = ha_api.get_sensor_value(ha_api.ENTITY_ID_STROMVERBRAUCH)
    show_message(f"S:{strom}")
    time.sleep(5)
    pv = ha_api.get_sensor_value(ha_api.ENTITY_ID_PV)
    show_message(f"PV:{pv}")
    time.sleep(5)


if __name__ == "__main__":
    main()