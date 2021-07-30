import pigpio
from time import sleep

def vcd_parse(name):
    timestamp = []
    lines = []
    with open(name, "r") as f:
        counter = 0
        for line in f:
            if line[0] == '#':
                counter += 1
            if counter >= 2:
                lines.append(line.strip())

    interval = []
    for i in range(2, len(lines), 2):
        a = int( lines[i-2][1:] )
        b = int( lines[i][1:] )
        interval.append(b - a)

    return interval

def decode(name):
    A = vcd_parse(name)
    thred = 700
    data = []
    for i in range(len(A)):
        if( (i & 1) != 1 ):
            if( A[i] > 700 ):
                data.append(1)
            else:
                data.append(0)

    with open(name[:-4]+".dat", 'w') as f:
        for i in range(1, len(data), 8):
            if i % 16 == 9:
                f.write('-'*8 + '\n')
            a = "".join(map(str, data[i:i+8]))
            f.write(a + '\n')

def pulse(on_us, off_us, pi):
    pi.write(3, 1)
    sleep(on_us*1e-6)
    pi.write(3, 0)
    sleep(off_us*1e-6)

def transmit(name):
    pi = pigpio.pi()

    A = vcd_parse(name)
    thred = 700
    data = []
    for i in range(len(A)):
        if( (i & 1) != 1 ):
            if( A[i] > 700 ):
                data.append(1)
            else:
                data.append(0)

    pi.hardware_clock(4, 38000)
    pulse(3370, 1640, pi)
    with open("t.bit", 'w') as f:
        for d in data[1:]:
            f.write(str(d)+"\n")
    #for d in data[1:]:
    #    if d == 1:
    #        pulse(440, 1280, pi)
    #    else:
    #        pulse(440, 490, pi)
    pi.hardware_clock(4, 0)
