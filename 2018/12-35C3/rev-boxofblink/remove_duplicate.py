import sys

if len(sys.argv) != 2:
    print("usage: %s [filename]" % (sys.argv[0]))
    sys.exit(0)


fp = open(sys.argv[1])

line = fp.readline()
index = 0
pre_a = 0
pre_b = 0
pre_c = 0
pre_d = 0
pre_e = 0
pre_f = 0
pre_g = 0
pre_h = 0
pre_i = 0
pre_j = 0
pre_k = 0
pre_l = 0
pre_m = 0
#pre_n = 0

while line:
#    print(line)
    items = line.split(',')
    ts = float(items[0])
    a = int(items[1])
    b = int(items[2])
    c = int(items[3])
    d = int(items[4])
    e = int(items[5])
    f = int(items[6])
    g = int(items[7])
    h = int(items[8])
    i = int(items[9])
    j = int(items[10])
    k = int(items[11])
    l = int(items[12])
    m = int(items[13])
 #   n = int(items[14])

    if a != pre_a or \
       b != pre_b or \
       c != pre_c or \
       d != pre_d or \
       e != pre_e or \
       f != pre_f or \
       g != pre_g or \
       h != pre_h or \
       i != pre_i or \
       j != pre_j or \
       k != pre_k or \
       l != pre_l or \
       m != pre_m:
#       n != pre_n:
       print("%.10f,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % (ts,a,b,c,d,e,f,g,h,i,j,k,l,m))
    
    pre_a = a
    pre_b = b
    pre_c = c
    pre_d = d
    pre_e = e
    pre_f = f
    pre_g = g
    pre_h = h
    pre_i = i
    pre_j = j
    pre_k = k
    pre_l = l
    pre_m = m
#    pre_n = n
    
    line = fp.readline()
    index = index + 1

    
