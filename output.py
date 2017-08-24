import scrollphathd as scroll
import sys
import time

scroll.set_brightness(0.2)
output = ' ' + ' '.join(sys.argv[1:])
scroll.clear()
scroll.flip(x=True, y=True)
scroll.write_string(output)

for _ in range(len(output)*10):
    scroll.scroll()
    scroll.show()
    time.sleep(0.05)
