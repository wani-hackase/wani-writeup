output = [225, 228, 219, 223, 220, 231, 205, 217, 224, 231, 228, 210, 208, 227, 220, 234, 236, 222, 232, 235, 227, 217, 223, 234]
sm = 2613

key = 'munchkyn'

subk0 = [x-ord(key[0]) for x in output]
print(subk0)
a = [x^ord(key[i%3])^ord(key[i//3]) for i, x in enumerate(subk0)]
print(a)


flag = ''
for i in range(3):
    for j in range(0, 24, 3):
        flag += chr(a[i+j])

print(sum(a))
print(flag)
