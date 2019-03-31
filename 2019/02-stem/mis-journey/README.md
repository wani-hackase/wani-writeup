# STEM CTF: Cyber Challenge 2019 "Journey to the Center of the File" writeup

## Description
`W(e( (h(a(v(e( (t(o( (g(o( (d(e(e(p(e(r)))))))))))))))))))`

[ZipFile](gb100-1-8a79568ebe1483695100d6a04525a7282673746b2c9d5e70b2f1729c42a85d42.zip)

## Solution

与えられたZipファイルを解凍すると flag というファイルが出てくる。ファイル形式を調べるとbzip2であったので更に解凍すると、Zipファイルが出てきた。Descriptionから察するに、この入れ子構造がひたすら続きそうだったが、とりあえず手作業で20回ほど続けてみた。すると、現れるファイルの形式は次の4つのパターンがあることがわかった。

* bzip2 -> 解凍
* gzip -> 解凍
* zip -> 解凍
* ASCIItext -> Base64でデコード -> 別のファイルとして保存

これらの処理をBashで書いて実行すると、最終的にASCIItextが残る。このとき、Base64でデコードできない旨のエラーが出るので、このエラーを終了条件とすればよい。この条件は、shebang の後ろに -e をつけると、エラーが出たときに処理を止めてくれるので簡単に書けた。
ちなみに-eは shebang の後ろでなくても、`set -e`でも良い。また、`set +e`で無効に出来る。

```bash
#!/bin/bash -e

while :
do
s=$(file flag | cut -f 2 -d ' ')

if [ "$s" = "ASCII" ]; then
    cat flag | base64 -d > flag2
    mv flag2 flag
    echo [+] ASCIItext
elif [ "$s" = "bzip2" ]; then
    bzip2 -d flag
    mv flag.out flag
    echo [+] bzip
elif [ "$s" = "gzip" ]; then
    mv flag flag.gz
    gzip -d flag.gz
    echo [+] gzip
elif [ "$s" = "Zip" ]; then
    mv flag flag.zip
    unzip flag.zip
    echo [+] zip
else
    break
fi

done

```

Flag : `MCA{Wh0_Needz_File_Extensions?}`
