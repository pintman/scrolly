import scrollphathd as scroll
import sys
import time

scroll.set_brightness(0.2)
output = ' ' + ' '.join(sys.argv[1:]) + (5*' ')
scroll.clear()
scroll.flip(x=True, y=True)
scroll.write_string(output)
print("buffer shape", scroll.get_buffer_shape())

width, height = scroll.get_buffer_shape()
for _ in range(width):
    scroll.scroll()
    scroll.show()
    time.sleep(0.05)
