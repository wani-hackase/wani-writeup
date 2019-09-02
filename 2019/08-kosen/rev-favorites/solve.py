def main():
    seed = 0x1234
    e = [0x62d5, 0x7b27, 0xc5d4, 0x11c4, 0x5d67, 0xa356, 0x5f84,
         0xbd67, 0xad04, 0x9a64, 0xefa6, 0x94d6, 0x2434, 0x0178]
    flag = ""
    for index in range(14):
        for i in range(0x7f-0x20):
            c = chr(0x20+i)
            res = encode(c, index, seed)
            if res == e[index]:
                print(c)
                flag += c
                seed = encode(c, index, seed)
    print("Kosen{%s}" % flag)

def encode(p1, p2, p3):
    p1 = ord(p1) & 0xff
    p2 = p2 & 0xffffffff
    p3 = p3 & 0xffffffff

    result = (((p1 >> 4) | (p1 & 0xf) << 4) + 1) ^ ((p2 >> 4) |
                                                    (~p2 << 4)) & 0xff | (p3 >> 4) << 8 ^ ((p3 >> 0xc) | (p3 << 4)) << 8
    return result & 0xffff


if __name__ == "__main__":
    main()
