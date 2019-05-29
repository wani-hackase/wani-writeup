# SECCON Beginners CTF 2019 "Seccompare" writeup

## problem

decompiled by Ghidra

```
undefined8 main(int iParm1,undefined8 *puParm2)

{
  int iVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  char local_38;
  undefined local_37;
  undefined local_36;
  undefined local_35;
  undefined local_34;
  undefined local_33;
  undefined local_32;
  undefined local_31;
  undefined local_30;
  undefined local_2f;
  undefined local_2e;
  undefined local_2d;
  undefined local_2c;
  undefined local_2b;
  undefined local_2a;
  undefined local_29;
  undefined local_28;
  undefined local_27;
  undefined local_26;
  undefined local_25;
  undefined local_24;
  undefined local_23;
  undefined local_22;
  undefined local_21;
  undefined local_20;
  undefined local_1f;
  undefined local_1e;
  undefined local_1d;
  undefined local_1c;
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (iParm1 < 2) {
    printf("usage: %s flag\n",*puParm2);
    uVar2 = 1;
  }
  else {
    local_38 = 'c';
    local_37 = 0x74;
    local_36 = 0x66;
    local_35 = 0x34;
    local_34 = 0x62;
    local_33 = 0x7b;
    local_32 = 0x35;
    local_31 = 0x74;
    local_30 = 0x72;
    local_2f = 0x31;
    local_2e = 0x6e;
    local_2d = 0x67;
    local_2c = 0x73;
    local_2b = 0x5f;
    local_2a = 0x31;
    local_29 = 0x73;
    local_28 = 0x5f;
    local_27 = 0x6e;
    local_26 = 0x30;
    local_25 = 0x74;
    local_24 = 0x5f;
    local_23 = 0x65;
    local_22 = 0x6e;
    local_21 = 0x30;
    local_20 = 0x75;
    local_1f = 0x67;
    local_1e = 0x68;
    local_1d = 0x7d;
    local_1c = 0;
    iVar1 = strcmp(&local_38,(char *)puParm2[1]);
    if (iVar1 == 0) {
      puts("correct");
    }
    else {
      puts("wrong");
    }
    uVar2 = 0;
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar2;
}
```

## solution

```python
t = ["74", "66", "34", "62", "7b", "35", "74", "72", "31", "6e", "67", "73", "5f", "31", "73", "5f", "6e", "30", "74", "5f", "65", "6e", "30", "75", "67", "68", "7d"]

a = "c"
for i in t:
    a = a + chr(int(i, 16))

print(a)

# ctf4b{5tr1ngs_1s_n0t_en0ugh}
```
