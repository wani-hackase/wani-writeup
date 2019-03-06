import sys
import numpy
from io import StringIO

def get_html(items):
    s = "<table>"
    for values in items:
        s += "<tr>"
        for val in values:
            if val == 1:
                s += '<td style="background-color: black; width: 5px; height: 5px;">a</td>'
            else:
                s += '<td style="background-color: white; width: 5px; height: 5px;">a</td>'

        s += "</tr>"        
    s += "</table>"
    return s

if len(sys.argv) != 2:
    print("usage: %s [filename]" % (sys.argv[0]))
    sys.exit(0)

fp = open(sys.argv[1])

line = fp.readline()

if line == "":
    sys.exit()

items = line.split(',')

pre_values = []

bitmap = []
for i in range(32):
    bitmap.append([0] * 128)

for i in range(len(items)):
    if i == 0:
        pre_values.append(float(items[i]))
    else:
        pre_values.append(int(items[i]))
        

index = 0
counter = 0
counter_clock = 0
file_index = 0
wfp = open("%04d.html" % file_index, "w")



while line:
    items = line.split(',')
    current_values = []
    for i in range(len(items)):
        if i == 0:
            current_values.append(float(items[i]))
        else:
            current_values.append(int(items[i]))

    if current_values[4] == 0 and pre_values[4] == 1:
        output = StringIO()
        numpy.savetxt(output, bitmap, delimiter="", fmt="%d")
        print(output.getvalue())
        sys.stdout.flush()
        print("renew")
        s = get_html(bitmap)
        wfp.write(s)
        wfp.close()
        file_index = file_index + 1
        wfp = open("%04d.html" % file_index, "w")
        
        bitmap = []
        for i in range(32):
            bitmap.append([0] * 128)
        counter = 0
        counter_clock = 0

    if current_values[1] == 1 and pre_values[1] == 0:
        counter_clock = 0
        counter = counter + 1

    if current_values[3] == 1 and pre_values[3] == 0:
        bitmap[counter][counter_clock] = (current_values[12] or current_values[13])
    
        counter_clock = counter_clock + 1
            
    pre_values = current_values
    line = fp.readline()
