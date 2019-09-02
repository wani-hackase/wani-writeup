#include<stdio.h>
undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  ushort seed;
  uint index;
  int index2;
  ushort auStack136 [16];
  byte flag_input [14];
  undefined local_59;
  undefined8 result;
  undefined8 local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  seed = 0x1234;
  puts("Do you know");
  puts(" --- the FLAG of this challenge?");
  puts(" --- my favorite anime?");
  puts(" --- my favorite character?");
  putchar(10);
  printf("Input your guess: ");
  __isoc99_scanf(&DAT_00102138,flag_input);
  local_59 = 0;
  index = 0;
  while ((int)index < 0xe) {
    seed = f(
      flag_input[(long)(int)index],
      index,
      seed,
      index);
    auStack136[index] = seed;
    index = index + 1;
  }
  result = 0;
  local_50 = 0;
  local_48 = 0;
  local_40 = 0;
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  index2 = 0;
  while (index2 < 0xe) {
    // ２バイト毎に書き込み
    sprintf(
      (char *)(&result + index2 * 4),
      "%04x", //4桁hexで出力
      auStack136[index2]);
    index2 = index2 + 1;
  }
  iVar1 = strcmp((char *)&result,first);
  if (iVar1 == 0) {
    printf("Congrats! The flag is KosenCTF{%s}!\n",flag_input);
  }
  else {
    iVar1 = strcmp((char *)&result,second);
    if (iVar1 == 0) {
      puts("Wow! Let\'s see it together now!");
    }
    else {
      iVar1 = strcmp((char *)&result,third);
      if (iVar1 == 0) {
        puts("Yes! Do you like too this?");
      }
      else {
        puts("No! You are not interested in me, are you?");
      }
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
    __stack_chk_fail();
  }
  return 0;
}

long f(byte chr,uint i,ushort s)

{
  return (ulong)(ushort)(
      ((chr >> 4) | ((chr & 0xf) << 4)) + 1 ^
      ((i >> 4) | (~i << 4)) &
      0xff |
      (s >> 4) << 8 ^
      (((s >> 0xc) | s << 4) << 8));
}

// first
// 62d57b27c5d411c45d67a3565f84bd67ad049a64efa694d624340178