# SECCON Beginners CTF 2020 "siblangs" writeup

## 問題

```
Well, they look so similar... siblangs.apk

(SHA-1 hash: c08d002c5837ad39d509a1d09ed623003ae97229)
```

## 解法

### Step 1. apktool

apk ファイルのリバースエンジニアリング問題

まずは apktool を使って中のファイルを取り出す

```
apktool d -s -o decompiled siblangs.apk
```

classes.dex が出てくるほか、`rg ctf4b`を実行すると assets/index.android.bundle がヒットする

### Step 2. assets/index.android.bundle の解析

ファイルを眺めていると `React` の文字が出てくるので `React Native` で作ったアプリだと思われる

ripgrep で ctf4b を検索すると出てきたところを抜粋

```javascript
function v() {
  var t;
  (0, l.default)(this, v);
  for (var o = arguments.length, n = new Array(o), c = 0; c < o; c++)
    n[c] = arguments[c];
  return (
    ((t = y.call.apply(y, [this].concat(n))).state = {
      flagVal: "ctf4b{",
      xored: [
        34,
        63,
        3,
        77,
        36,
        20,
        24,
        8,
        25,
        71,
        110,
        81,
        64,
        87,
        30,
        33,
        81,
        15,
        39,
        90,
        17,
        27,
      ],
    }),
    (t.handleFlagChange = function (o) {
      t.setState({ flagVal: o });
    }),
    (t.onPressValidateFirstHalf = function () {
      if ("ios" === h.Platform.OS) {
        for (
          var o = "AKeyFor" + h.Platform.OS + "10.3",
            l = t.state.flagVal,
            n = 0;
          n < t.state.xored.length;
          n++
        )
          if (
            t.state.xored[n] !==
            parseInt(l.charCodeAt(n) ^ o.charCodeAt(n % o.length), 10)
          )
            return void h.Alert.alert("Validation A Failed", "Try again...");
        h.Alert.alert(
          "Validation A Succeeded",
          "Great! Have you checked the other one?"
        );
      } else
        h.Alert.alert(
          "Sorry!",
          "Run this app on iOS to validate! Or you can try the other one :)"
        );
    }),
    (t.onPressValidateLastHalf = function () {
      "android" === h.Platform.OS
        ? p.default.validate(t.state.flagVal, function (t) {
            t
              ? h.Alert.alert(
                  "Validation B Succeeded",
                  "Great! Have you checked the other one?"
                )
              : h.Alert.alert(
                  "Validation B Failed",
                  "Learn once, write anywhere ... anywhere?"
                );
          })
        : h.Alert.alert(
            "Sorry!",
            "Run this app on Android to validate! Or you can try the other one :)"
          );
    }),
    t
  );
}
```

onPressValidateFirstHalf で入力を XOR でチェックしているのでもとに戻す

```python
a = [34,63,3,77,36,20,24,8,25,71,110,81,64,87,30,33,81,15,39,90,17,27]

key = "AKeyForios10.3"

ans = ""

for i in range(len(a)):
    ans += chr(a[i] ^ ord(key[i % len(key)]))

print(ans)

# ctf4b{jav4_and_j4va5cr
```

onPressValidateLastHalf で p.default.validate を呼んでいるがこのファイルの中にはないので java で処理していると見当をつけて先程出てきた classes.dex を解析する

### Step 3. classes.dex の解析

#### dex2jar で dex ファイルを jar ファイルに戻す

<https://sourceforge.net/projects/dex2jar/>

```
chmod +x d2j-dex2jar.sh
./d2j-dex2jar.sh ../classes.dex
```

classes-dex2jar.jar が生成される

#### JD-GUI で javaのソースコードを調べる

<http://java-decompiler.github.io/>

JD-GUI でclasses-dex2jar.jarを開くと`es.o0i.challengeapp/nativemodule/ValidateFlagModule`にてValidateするコードがある

```java
package es.o0i.challengeapp.nativemodule;
import com.facebook.react.bridge.Callback;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
public class ValidateFlagModule extends ReactContextBaseJavaModule {
  private static final int GCM_IV_LENGTH = 12;
  private final ReactApplicationContext reactContext;
  private final SecretKey secretKey = new SecretKeySpec("IncrediblySecure".getBytes(), 0, 16, "AES");
  private final SecureRandom secureRandom = new SecureRandom();
  public ValidateFlagModule(ReactApplicationContext paramReactApplicationContext) {
    super(paramReactApplicationContext);
    this.reactContext = paramReactApplicationContext;
  }
  public String getName() {
    return "ValidateFlagModule";
  }
  @ReactMethod
  public void validate(String paramString, Callback paramCallback) {
    byte[] arrayOfByte = new byte[43];
    arrayOfByte[0] = 95;
    arrayOfByte[1] = -59;
    arrayOfByte[2] = -20;
    arrayOfByte[3] = -93;
    arrayOfByte[4] = -70;
    arrayOfByte[5] = 0;
    arrayOfByte[6] = -32;
    arrayOfByte[7] = -93;
    arrayOfByte[8] = -23;
    arrayOfByte[9] = 63;
    arrayOfByte[10] = -9;
    arrayOfByte[11] = 60;
    arrayOfByte[12] = 86;
    arrayOfByte[13] = 123;
    arrayOfByte[14] = -61;
    arrayOfByte[15] = -8;
    arrayOfByte[16] = 17;
    arrayOfByte[17] = -113;
    arrayOfByte[18] = -106;
    arrayOfByte[19] = 28;
    arrayOfByte[20] = 99;
    arrayOfByte[21] = -72;
    arrayOfByte[22] = -3;
    arrayOfByte[23] = 1;
    arrayOfByte[24] = -41;
    arrayOfByte[25] = -123;
    arrayOfByte[26] = 17;
    arrayOfByte[27] = 93;
    arrayOfByte[28] = -36;
    arrayOfByte[29] = 45;
    arrayOfByte[30] = 18;
    arrayOfByte[31] = 71;
    arrayOfByte[32] = 61;
    arrayOfByte[33] = 70;
    arrayOfByte[34] = -117;
    arrayOfByte[35] = -55;
    arrayOfByte[36] = 107;
    arrayOfByte[37] = -75;
    arrayOfByte[38] = -89;
    arrayOfByte[39] = 3;
    arrayOfByte[40] = 94;
    arrayOfByte[41] = -71;
    arrayOfByte[42] = 30;
    try {
      Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
      GCMParameterSpec gCMParameterSpec = new GCMParameterSpec(128, arrayOfByte, 0, 12);
      cipher.init(2, this.secretKey, gCMParameterSpec);
      arrayOfByte = cipher.doFinal(arrayOfByte, 12, arrayOfByte.length - 12);
      byte[] arrayOfByte1 = paramString.getBytes();
      for (int i = 0;; i++) {
        if (i < arrayOfByte.length) {
          if (arrayOfByte1[i + 22] != arrayOfByte[i]) {
            paramCallback.invoke(new Object[] { Boolean.valueOf(false) });
            return;
          }
        } else {
          paramCallback.invoke(new Object[] { Boolean.valueOf(true) });
          return;
        }
      }
    } catch (Exception exception) {
      paramCallback.invoke(new Object[] { Boolean.valueOf(false) });
      return;
    }
  }
}
```

arrayOfByte を出力して正しいフラグを調べる

```java
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class Generate{
  public static void main(String[] args){
    SecretKey secretKey = new SecretKeySpec("IncrediblySecure".getBytes(), 0, 16, "AES");
    byte[] arrayOfByte = new byte[43];
    arrayOfByte[0] = 95;
    arrayOfByte[1] = -59;
    arrayOfByte[2] = -20;
    arrayOfByte[3] = -93;
    arrayOfByte[4] = -70;
    arrayOfByte[5] = 0;
    arrayOfByte[6] = -32;
    arrayOfByte[7] = -93;
    arrayOfByte[8] = -23;
    arrayOfByte[9] = 63;
    arrayOfByte[10] = -9;
    arrayOfByte[11] = 60;
    arrayOfByte[12] = 86;
    arrayOfByte[13] = 123;
    arrayOfByte[14] = -61;
    arrayOfByte[15] = -8;
    arrayOfByte[16] = 17;
    arrayOfByte[17] = -113;
    arrayOfByte[18] = -106;
    arrayOfByte[19] = 28;
    arrayOfByte[20] = 99;
    arrayOfByte[21] = -72;
    arrayOfByte[22] = -3;
    arrayOfByte[23] = 1;
    arrayOfByte[24] = -41;
    arrayOfByte[25] = -123;
    arrayOfByte[26] = 17;
    arrayOfByte[27] = 93;
    arrayOfByte[28] = -36;
    arrayOfByte[29] = 45;
    arrayOfByte[30] = 18;
    arrayOfByte[31] = 71;
    arrayOfByte[32] = 61;
    arrayOfByte[33] = 70;
    arrayOfByte[34] = -117;
    arrayOfByte[35] = -55;
    arrayOfByte[36] = 107;
    arrayOfByte[37] = -75;
    arrayOfByte[38] = -89;
    arrayOfByte[39] = 3;
    arrayOfByte[40] = 94;
    arrayOfByte[41] = -71;
    arrayOfByte[42] = 30;
    System.out.println(arrayOfByte);
    try {
      Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
      GCMParameterSpec gCMParameterSpec = new GCMParameterSpec(128, arrayOfByte, 0, 12);
      cipher.init(2, secretKey, gCMParameterSpec);
      arrayOfByte = cipher.doFinal(arrayOfByte, 12, arrayOfByte.length - 12);
      for (int i = 0;; i++) {
        if (i < arrayOfByte.length) {
          System.out.println(arrayOfByte[i]);
        }
      }
    } catch (Exception exception) {
      System.out.println("Fail");
      return;
    }
  }
}
```

```python
b = [49, 112, 116, 95, 51, 118, 101, 114, 121, 119, 104, 101, 114, 101, 125]

ans = ""

for i in range(len(b)):
    ans += chr(b[i])
    print(ans)

print(ans)

# 1pt_3verywhere}
```

よってフラグは

```
ctf4b{jav4_and_j4va5cr1pt_3verywhere}
```
