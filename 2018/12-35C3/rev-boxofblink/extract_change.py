import sys


ignores = [0]

if len(sys.argv) != 2:
    print("usage: %s [filename]" % (sys.argv[0]))
    sys.exit(0)


fp = open(sys.argv[1])

line = fp.readline()

if line == "":
    sys.exit()

items = line.split(',')

pre_values = []

for i in range(len(items)):
    if i == 0:
        pre_values.append(float(items[i]))
    else:
        pre_values.append(int(items[i]))
        


index = 0

while line:
    items = line.split(',')
    current_values = []
    for i in range(len(items)):
        if i == 0:
            current_values.append(float(items[i]))
        else:
            current_values.append(int(items[i]))
            
    if current_values[1:-1] != pre_values[1:-1]:
        for i in range(len(pre_values)):
            if i == 0:
                print("%.10f" % (pre_values[i]), end="")
            else:
                print(",%d" % (pre_values[i]), end="")
        print("")

        for i in range(len(current_values)):
            if i == 0:
                print("%.10f" % (current_values[i]), end="")
            else:
                print(",%d" % (current_values[i]), end="")
        print("")
        
    pre_values = current_values
    line = fp.readline()
    index = index + 1
#    if index == 100000:
#        break

    
