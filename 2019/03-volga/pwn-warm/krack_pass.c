#include <stdio.h>
#include <ctype.h>

int main()
{
  uint8_t c, tmp;
  c = 0x76;
  
  putchar(c);  
  tmp = 0x4e;
  c = c ^ tmp;
  
  putchar(c);
  tmp = 0x1e;
  c = c ^ tmp;

  //  putchar(c);  
  //  tmp = 0x43;
  //  c = c ^ tmp;

  putchar(c);  
  tmp = 0x15;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x5e;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x1c;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x21;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x01;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x34;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x07;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x35;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x11;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x37;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x3c;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x72;
  c = c ^ tmp;

  putchar(c);  
  tmp = 0x47;
  c = c ^ tmp;

  putchar(c);
}
