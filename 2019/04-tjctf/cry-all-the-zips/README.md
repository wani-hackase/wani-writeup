# TJCTF 2019 "All the Zips" writeup

## check problem

```
140 zips in the zip, all protected by a dictionary word.

All the zips
```

I get 140 zip file.

## solve problem

It is said that password is a dictionary word.

I try to crack password by fcrackzip.

```
$ fcrackzip -u -D -p /usr/share/dict/words zip0.zip
PASSWORD FOUND!!!!: pw == how
```

```
$ unzip -o -P "how" zip0.zip ; cat flag.txt
Archive:  zip0.zip
extracting: flag.txt
whew
```

I can easily get password, and unzip file.

Then, let's try all 140 zip files!

```bash
#!/bin/bash

for i in {0..139} ; do

  fcrackzip -u -D -p ./words zip$i.zip >> pass.log

  echo "zip$i.zip" >> pass.log

done
```

```bash
#!/bin/bash

unzip -o -P "how" zip0.zip ; cat flag.txt >> flag.log ; echo "" >> flag.log

unzip -o -P "to" zip1.zip ; cat flag.txt >> flag.log ; echo "" >> flag.log

unzip -o -P "establish" zip2.zip ; cat flag.txt >> flag.log ; echo "" >> flag.log

・・・
```

I can get flag in zip85.zip.

```
$ unzip -o -P "every" zip85.zip ; cat flag.txt
tjctf{sl4m_1_d0wn_s0_that_it5_heard}
```
