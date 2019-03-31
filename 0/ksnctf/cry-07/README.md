# Ksnctf 7 Programming

<https://ksnctf.sweetduet.info/problem/7>

```cpp
#include   	 	<stdio.h>

     	#include  	  <string.h>

  int   	  	main
	()
   {   	const		char 	*
s	=
 "     	    "
"0123456789"
"     "

"		   "
"			         							  				 			 "
	 "ABCDEFGHIJ" 	;
	 printf	(
   	  "%c"	,		strlen
(s)
 );  int  i	  =	020000000	+	001000000	+
000600000
  +000040000
+000007000
+000000500
+000000020
+000000002  	;
   	  	printf		(
	"%s"
     	,&  	 i
	)
;
	long
    long
			   							  				 		 	 					 l
	  =

  2LL
	    *
 	11LL

	  	 *
 	229LL

	    *
 	614741LL

	    *
 	9576751LL

	  	 +
 	5LL


 	;


 	printf
     	  	  (
	  "%s"

     	    ,


    &


     		l


    )


     		 		;


    float


     	f		 =


     1.0962664770776731080774868826855754386638240000e-38f


     ;


     printf(		"%s"


     	 ,
	    &f
 )
    ;
	double

d     		 			=
	6.7386412564254706622868098890859398199406890000e-308
 ;
  printf
("%s"
,&d);
}
```

謎の cpp コード。

<https://ja.wikipedia.org/wiki/Whitespace>

難解プログラミング言語の Whitespace というものらしい。

Web IDE があるのでそこで実行

<https://vii5ard.github.io/whitespace/>

push 33355524 で jz label_0 が実行される

他の PIN では printc が実行される

```
PIN: 33355524
OK
FLAG_XXXXXXXXXXXXXXXX
```

flag get
