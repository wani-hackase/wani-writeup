undefined4 FUN_000109ec(void)
{
  int __c;
  FILE *__stream;
  char acStack220 [100];
  char acStack120 [100];
  int local_14;
  local_14 = __stack_chk_guard;
  setvbuf(stdout,(char *)0x0,2,0);
  while( true ) {
    while( true ) {
      FUN_000108f0(acStack120);
      puts("Hi there! I\'ve been waiting for your password!");
      gets(acStack220);
      __c = FUN_00010788(acStack220);
      if (__c == 0){
	break;
      }
      FUN_00010978(1,0);
    }
    __stream = fopen(acStack120,"rb");
    if (__stream != (FILE *)0x0){
      break;
    }
    FUN_00010978(2,acStack120);
  }
 
  while (__c = _IO_getc((_IO_FILE *)__stream), __c != -1) {
    putchar(__c);
  }
  fclose(__stream);
  if (local_14 == __stack_chk_guard) {
    return 0;
  }
  /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
