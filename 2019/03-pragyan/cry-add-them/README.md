# Pragyan CTF 2019 "Add them Sneaky Polynomials" writeup

## Description

Rahul, the geek boy of his class, doesn't like doing things the conventional way. He's just learned polynomials in class, and wants to prove a point to his friend Sandhya. But Sandhya is sitting in the first bench, so Ram decides to write what he wants to convey on a chit and pass it through the guys sitting in front of him. The guys in between try to read it, but do not understand. Sadly, nor does Sandhya. Can you help him out?

## Solution

多項式 p, q, r が与えられるが他に手がかりは無いので、多項式としてではなくxの指数に注目する。
ヒントに`XOR is your best friend`とあったので、「x^i」 を 「i bit 目に1が立っている」（e.g.  「x^3 + x^2  + 1」 → 「1101」）とみなしてp, q, r のXORを取ってみる。指数 i が現れた回数をカウントし、奇数回出現したならば 1 、偶数回出現したならば 0、というようにして i bit 目を決めていった。

```python
from collections import Counter

p = ['406', '405', '402', '399', '397', '391', '390', '387', '386', '378', '374', '372', '371', '369', '367', '364', '360', '358', '357', '352', '350', '345', '344', '341', '336', '335', '334', '333', '331', '330', '329', '328', '327', '324', '322', '320', '314', '311', '308', '307', '303', '300', '299', '296', '295', '290', '289', '287', '279', '271', '266', '264', '262', '260', '257', '256', '252', '249', '248', '246', '243', '239', '238', '236', '233', '230', '227', '225', '223', '222', '220', '218', '216', '215', '209', '208', '207', '204', '202', '199', '190', '189', '185', '184', '180', '177', '176', '175', '172', '167', '166', '162', '160', '159', '155', '154', '149', '147', '143', '137', '135', '131', '129', '126', '124', '122', '116', '110', '108', '105', '104', '100', '99', '97', '94', '93', '90', '88', '87', '86', '85', '83', '75', '73', '69', '63', '62', '57', '54', '51', '44', '41', '38', '37', '36', '34', '29', '28', '26', '25', '21', '20', '19', '16', '15', '14', '13', '6', '5', '2']
q = ['399', '398', '396', '393', '392', '391', '388', '386', '384', '381', '377', '376', '368', '364', '360', '355', '354', '353', '352', '348', '346', '345', '344', '343', '335', '334', '329', '326', '325', '321', '318', '317', '315', '314', '311', '307', '306', '304', '300', '296', '293', '291', '282', '277', '270', '263', '261', '260', '256', '254', '253', '252', '251', '248', '245', '242', '241', '239', '238', '236', '232', '226', '225', '222', '220', '219', '214', '209', '208', '207', '206', '202', '200', '196', '191', '190', '186', '181', '180', '178', '177', '169', '168', '165', '164', '163', '162', '161', '159', '157', '156', '151', '149', '148', '147', '146', '144', '141', '140', '138', '137', '136', '134', '133', '132', '130', '129', '128', '126', '123', '121', '113', '109', '103', '101', '100', '95', '93', '91', '85', '84', '81', '74', '73', '71', '68', '67', '54', '52', '51', '50', '48', '46', '45', '43', '39', '35', '32', '31', '30', '29', '21', '15', '14', '9', '8', '5', '4', '2', '0']
r = ['404', '402', '396', '389', '387', '386', '384', '382', '376', '373', '367', '366', '365', '362', '361', '358', '356', '355', '354', '353', '352', '349', '348', '347', '345', '343', '340', '334', '332', '331', '328', '327', '326', '322', '317', '316', '314', '313', '312', '310', '309', '308', '305', '304', '303', '301', '300', '299', '296', '295', '292', '291', '290', '288', '287', '286', '285', '283', '279', '278', '274', '271', '269', '268', '266', '265', '263', '261', '260', '259', '258', '256', '254', '252', '251', '250', '249', '244', '243', '242', '237', '236', '228', '225', '224', '223', '222', '221', '215', '214', '213', '212', '205', '201', '200', '199', '197', '193', '192', '191', '190', '189', '188', '187', '182', '180', '175', '174', '173', '167', '166', '163', '158', '156', '155', '153', '151', '150', '149', '143', '142', '140', '139', '136', '135', '133', '129', '126', '125', '123', '121', '118', '117', '116', '115', '113', '110', '106', '105', '104', '103', '102', '98', '95', '92', '89', '87', '85', '81', '80', '77', '76', '75', '74', '71', '70', '67', '66', '64', '63', '60', '59', '58', '56', '54', '53', '48', '44', '41', '39', '38', '35', '34', '31', '29', '28', '27', '22', '21', '20', '17', '14', '12', '11', '10', '9', '6', '4', '3', '1', '0']

exp = []
for x in p:
    exp.append(x)
for x in q:
    exp.append(x)
for x in r:
    exp.append(x)

cnt = Counter(exp)

xor = []
for i in range(408):
    if cnt[str(i)]%2:
        xor.append('1')
    else:
        xor.append('0')

xor = ''.join(reversed(xor))
xor = hex(int(xor, 2))
print(xor)

flg = ''
for a, b in zip(xor[2::2], xor[3::2]):
    flg += chr(int(a+b, 16))
print(flg)

```

後は得られた2進数の値を文字へと変換してFlag 獲得。

Flag : `pctf{f1n1t3_f13lds_4r3_m0r3_us3ful_th4n_y0u_th1nk}`