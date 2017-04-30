import scrollphathd as scroll
import mosquitto
import time
import subprocess

class Scrolly:
    def __init__(self, host="cubietruck"):
        self.topic_method = {
            "scrolly/write/scroll": self.write_scroll,            
            "scrolly/write": self.write,
            "scrolly/power": self.power}
        
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

        self.mos.loop_forever()

    def on_message(self, mosq, userdata, msg):
        print("msg received", msg.topic, msg.payload)

        if msg.topic in self.topic_method:
            meth = self.topic_method[msg.topic]
            meth(str(msg.payload, encoding="UTF8"))            

    def write_scroll(self, message, wait=0.08):
        scroll.clear()
        scroll.write_string(message, monospaced=True)
        i = len(message*6)
        for i in range(i):
            scroll.scroll()
            scroll.show()
            time.sleep(wait)

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

sc = Scrolly()

