
ulong checkpw(void)

{
  int iVar1;
  int iVar2;
  ulong uVar3;
  char *__s2;
  char buf [104];
  char *local_18;
  ulong local_10;
  
  iVar1 = rand();
  iVar2 = rand();
  uVar3 = (long)iVar2 ^ (long)iVar1 << 0x20;
  local_10 = uVar3;
  puts("Enter the password");
  fgets(buf,0x100,stdin);
  local_18 = strchr(buf,10);
  if (local_18 != (char *)0x0) {
    *local_18 = 0;
  }
  __s2 = getenv("SECUREPASSWORD");
  iVar1 = strcmp(buf, __s2);
  if (iVar1 != 0) {
    stakcheck(uVar3,local_10);
  } else {
    stakcheck(uVar3,local_10);
  }
  return (ulong)(iVar1 == 0);
}



/* WARNING: Removing unreachable block (ram,0x0040119d) */
/* WARNING: Removing unreachable block (ram,0x004011a9) */

void deregister_tm_clones(void)

{
  return;
}


void FUN_00401020(void)

{
                    /* WARNING: Treating indirect jump as call */
  (*(code *)(undefined *)0x0)();
  return;
}



int init(EVP_PKEY_CTX *ctx)

{
  int extraout_EAX;
  int local_18 [2];
  int local_10;
  
  gettimeofday((timeval *)local_18,(__timezone_ptr_t)0x0);
  srand(local_18[0] * 1000000 + local_10);
  return extraout_EAX;
}



void logit(void)

{
  FILE *__stream;
  char *pcVar1;
  int local_ac;
  char local_a8 [48];
  undefined8 local_78;
  undefined8 local_70;
  MD5_CTX local_68;
  
  local_ac = rand();
  MD5_Init(&local_68);
  MD5_Update(&local_68,&local_ac,4);
  MD5_Final((uchar *)&local_78,&local_68);
  sprintf(local_a8,"%lx%lx",local_78,local_70);
  puts("You.dumbass is not in the sudoers file.  This incident will be reported.");
  printf("Incident UUID: %s\n",local_a8);
  __stream = fopen("/dev/null","w");
  if (__stream != (FILE *)0x0) {
    if (times == 0) {
      pcVar1 = "";
    }else{
      pcVar1 = "(Again)";
    }
    
    fprintf(__stream,"Incident %s: That dumbass forgot his password %s\n",local_a8,pcVar1);
    fclose(__stream);
    times = times + 1;
  }
  return;
}


void main(EVP_PKEY_CTX *pEParm1)

{
  int iVar1;
  int count;
  
  init(pEParm1);
  puts("Welcome to the Super dooper securer shell! Now with dynamic stack canaries and incidentreporting!");
  count = 0;
  do {
    if (count > 2){
LAB_00401487:
      puts("\nToo many wrong attempts, try again later");
      return;
    }
    
    if (count != 0) {
      printf("\nattempt #%i\n",(ulong)(count + 1));
    }
    
    iVar1 = checkpw();
    if (iVar1 != 0) {
      shell();
      goto LAB_00401487;
    }
    logit();
    count = count + 1;
  } while( true );
}


/* WARNING: Removing unreachable block (ram,0x004011df) */
/* WARNING: Removing unreachable block (ram,0x004011eb) */

void register_tm_clones(void)

{
  return;
}


void shell(void)

{
  execve("/bin/bash",(char **)0x0,(char **)0x0);
                    /* WARNING: Subroutine does not return */
  exit(0);
}


void stakcheck(long lParm1,long lParm2)

{
  if (lParm1 == lParm2) {
    return;
  }
  puts("LARRY THE CANARY IS DEAD");
                    /* WARNING: Subroutine does not return */
  exit(1);
}

