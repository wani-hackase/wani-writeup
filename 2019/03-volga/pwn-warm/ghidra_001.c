undefined4 FUN_00010788(byte *pbParm1)
{
  size_t sVar1;
  undefined4 uVar2;
 
  sVar1 = strlen((char *)pbParm1);
  if (sVar1 < 0x10) {
    uVar2 = 1;
  }else {
    if (((((*pbParm1 == 0x76) && ((pbParm1[1] ^ *pbParm1) == 0x4e)) &&
	  ((pbParm1[2] ^ pbParm1[1]) == 0x1e)) &&
	 ((((pbParm1[3] ^ pbParm1[2]) == 0x15 && ((pbParm1[4] ^ pbParm1[3]) == 0x5e)) &&
	   (((pbParm1[5] ^ pbParm1[4]) == 0x1c &&
	     (((pbParm1[6] ^ pbParm1[5]) == 0x21 && ((pbParm1[7] ^ pbParm1[6]) == 1)))))))) &&
	(((pbParm1[8] ^ pbParm1[7]) == 0x34 &&
	  ((((((pbParm1[9] ^ pbParm1[8]) == 7 && ((pbParm1[10] ^ pbParm1[9]) == 0x35)) &&
	      ((pbParm1[0xb] ^ pbParm1[10]) == 0x11)) &&
	     (((pbParm1[0xc] ^ pbParm1[0xb]) == 0x37 && ((pbParm1[0xd] ^ pbParm1[0xc]) == 0x3c))))&&
	    (((pbParm1[0xe] ^ pbParm1[0xd]) == 0x72 && ((pbParm1[0xf] ^ pbParm1[0xe]) ==0x47)))))))) {
      uVar2 = 0;
    } else {
      uVar2 = 2;
    }
  }
  return uVar2;
}
