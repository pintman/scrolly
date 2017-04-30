import scrollphathd as scroll
from scrollphathd.fonts import font5x7
import mosquitto
import time
import subprocess
import threading

class Scrolly:
    def __init__(self, host="cubietruck"):
        self.topic_method = {
            "scrolly/write/scroll": self.write_scroll,            
            "scrolly/write": self.write,
            "scrolly/power": self.power,
            "scrolly/brightness": self.set_brightness}
        
        scroll.flip(x=True, y=True)
        scroll.clear()
        scroll.write_string("on")
        scroll.show()
        
        self.mos = mosquitto.Mosquitto()
        self.mos.on_message = self.on_message
        self.debug("connecting to " + host)
        self.mos.connect(host)
        self.mos.publish("scrolly/power", 1)
        self.mos.subscribe("scrolly/#")

        self.stop_event = threading.Event()
        
        self.mos.loop_forever()

    def on_message(self, mosq, userdata, msg):
        print("msg received", msg.topic, msg.payload)

        if msg.topic in self.topic_method:
            self.stop_event.set()
            meth = self.topic_method[msg.topic]
            meth(str(msg.payload, encoding="UTF8"))            

    def write_scroll(self, message, wait=0.08):
        scroll.clear()
        scroll.write_string(message, x=0, y=0, font=font5x7)

        self.stop_event.clear()
        th = threading.Thread(target=self._write_scroll_worker,
                              args=(message, wait))
        th.start()

    def _write_scroll_worker(self, msg, wait_time):
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
            self.write("off")
            subprocess.call("sudo shutdown now", shell=True)

    def write(self, message):
        scroll.clear()
        scroll.write_string(message)
        scroll.show()

    def debug(self, msg):
        self.mos.publish("scrolly/debug", msg)


        
if __name__ == "__main__":
    sc = Scrolly()

