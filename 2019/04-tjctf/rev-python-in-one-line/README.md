# TJCTF 2019 "python in one line"

## Description
It's not code golf but it's something...

[one.py]() This is printed when you input the flag:

 .. - / .. ... -. - / -- --- .-. ... / -.-. --- -.. .

## Solution

The flag is encoded by the script below.


``` python
# one.py

print(
' '.join(
  [
    {
      'a':'...-',
      'b':'--..',
      'c':'/',
      'd':'-.--',
      'e':'.-.',
      'f':'...',
      'g':'.-..',
      'h':'--',
      'i':'---',
      'j':'-',
      'k':'-..-',
      'l':'-..',
      'm':'..',
      'n':'.--',
      'o':'-.-.',
      'p':'--.-',
      'q':'-.-',
      'r':'.-',
      's':'-...',
      't':'..',
      'u':'....',
      'v':'--.',
      'w':'.---',
      'y':'..-.',
      'x':'..-',
      'z':'.--.',
      '{':'-.',
      '}':'.'
    }[i] for i in input('What do you want to secrify? ')
  ]))
```

To decode the flag, we have to write decoding script.

The decoding Python code looks like this:

``` python
#solve.py

flag = ".. - / .. ... -. - / -- --- .-. ... / -.-. --- -.. ."

dict_a = {
  'a':'...-',
  'b':'--..',
  'c':'/',
  'd':'-.--',
  'e':'.-.',
  'f':'...',
  'g':'.-..',
  'h':'--',
  'i':'---',
  'j':'-',
  'k':'-..-',
  'l':'-..',
  'm':'..',
  'n':'.--',
  'o':'-.-.',
  'p':'--.-',
  'q':'-.-',
  'r':'.-',
  's':'-...',
  't':'..',
  'u':'....',
  'v':'--.',
  'w':'.---',
  'y':'..-.',
  'x':'..-',
  'z':'.--.',
  '{':'-.',
  '}':'.'
}

flag = flag.split(' ')

# Replace the key and value in dict_a.
dict_b = {v:k for k, v in dict_a.items()}

print(' '.join([dict_b[i] for i in flag]))

```
### output
```
$ python solve.py
tjctf{jchiefcoil}
```
