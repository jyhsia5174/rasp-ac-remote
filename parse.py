from time import sleep

def vcd_parse(name):
    lines = []
    with open(name, "r") as f:
        counter = 0
        stamp = ""
        for line in f:
            if line[0] == '#':
                stamp = line.strip()
                counter += 1
            if counter >= 2:
                if line[0] != '#':
                    now = line.strip()
                    if now[-1] == 'C':
                        lines.append(stamp)
                        lines.append(now)

    interval = []
    for i in range(2, len(lines), 2):
        a = int( lines[i-2][1:] )
        b = int( lines[i][1:] )
        interval.append(b - a)

    print("len: "+ str( len(interval) ))
    print(interval)
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

