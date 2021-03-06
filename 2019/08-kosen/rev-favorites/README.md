# interkosenCTF "favorites" reversing

## 問題

64bitバイナリが渡されるのでGDB, GHIDRAで解析していく。

GHIDRAでELFファイルをでコンパイルしたものを見ると、入力した文字列の各文字に対してある関数f()を
適用してめちゃくちゃな値にしている。

その後、データ領域の文字列(first, second, third)と比較して一致しているかを確認している。

コードを見るにfirstがFLAGを暗号化したものだとわかる。

```c
seed = 0x1234;

// 0xe=14回ループしているのでフラグの中身は14文字
while ((int)index < 0xe) {
    seed = f(
      flag_input[(long)(int)index],
      index,
      seed,
      index);
    auStack136[index] = seed;
    index = index + 1;
  }
```

関数f()が行っている暗号化がかなりややこしい。GDBとかでやろうとするとかなりしんどそう。

```c
long f(byte chr,uint i,ushort s)

{
  return (ulong)(ushort)(
      ((chr >> 4) | ((chr & 0xf) << 4)) + 1 ^
      ((i >> 4) | (~i << 4)) &
      0xff |
      (s >> 4) << 8 ^
      (((s >> 0xc) | s << 4) << 8));
}
```

第一引数に入力文字、第二引数に乱数（初期値は0x1234）、第三引数に文字列のインデックスが入る。
返り値として乱数がくるので次のループでその値をまた第二引数に取っている。

## 解法

```c
while (index2 < 0xe) {
    // ２バイト毎に書き込み
    sprintf(
      (char *)(&result + index2 * 4),
      "%04x", //4桁hexで出力
      auStack136[index2]);
    index2 = index2 + 1;
  }
```

入力文字列から作った乱数をauStack136からresultへ4桁ずつのHEX文字列にして書き写している。

変換例

|入力文字|auStack136|result|
|:-----:|:-------:|:----:|
|"A"|0x62d5|"62d5"|
|文字|数値|文字列|

暗号化されたFLAGはわかっているので、

1. 入力文字列の前から1文字ずつ総当りする。

1. 長さ4の文字列が出来るので変換結果が暗号化されたものと一致するか確認する。

1. 一致した場合、関数f()の返り値を次のループの引数として渡す。

これでFLAGが取り出せる。

FLAG: `Kosen{Bl00m_1n70_Y0u}`

## 感想
* ビット演算を行っているのでpythonで解答コードを書くときにレジスタの幅とか考えないといけないのかな？
とか考えていたが、この問題ではあまり関係なかった。

* GHIDRAでコンパイルしたときに定義では３個の引数しか取っていない`f()`が、呼び出しの際には引数が
4個も入っていたのが謎だった。

![image](https://github.com/wani-hackase/wani-writeup/blob/master/2019/08-kosen/rev-favorites/Screenshot%20from%202019-09-03%2002-10-12.png)
