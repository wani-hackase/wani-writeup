### 解法
- https://moar_horse_2.tjctf.org/ にアクセスするとしてBACKWORD, FORWORDのボタンを押していくとファイル名は変わっている。
- それ以外の特徴的なことはファイル名は特徴的でUUIDのフォーマットに沿っている。
- そこで https://moar_horse_2.tjctf.org/ このディレクトリ以下にファイル名がUUIDのフォーマットに沿ったファイルがあると想定して以下のwgetコマンドを実行する。
- そうすると、かなり多くのファイルがダウンロードされるので、その中にflagとなるものはないかをgrepしていくと、flagが見つかる。

```bash
wget https://moar_horse_2.tjctf.org/ -rl0 # 再帰的にファイルをダウンロード(32771件のファイルをダウンロードするのに相当時間がかかる)
find -type f -print0 | xargs -0 more | cat | grep ctf # ファイル内を全て探索する
```

### 参考
- `llコマンド`で改行してファイルを表示して, `wc -lコマンド`で行数をカウント.
```bash
ls -1 | wc -l
```

- `wgetコマンド`
```text
$ wget -h
GNU Wget 1.19.4, 非対話的ネットワーク転送ソフト
使い方: wget [オプション]... [URL]...

長いオプションで不可欠な引数は短いオプションでも不可欠です。

スタートアップ:
  -V,  --version                   バージョン情報を表示して終了する
  -h,  --help                      このヘルプを表示する
  -b,  --background                スタート後にバックグラウンドに移行する
  -e,  --execute=COMMAND           `.wgetrc'形式のコマンドを実行する

ログと入力ファイル:
  -o,  --output-file=FILE          ログを FILE に出力する
  -a,  --append-output=FILE        メッセージを FILE に追記する
  -d,  --debug                     デバッグ情報を表示する
  -q,  --quiet                     何も出力しない
  -v,  --verbose                   冗長な出力をする (デフォルト)
  -nv, --no-verbose                冗長ではなくする
       --report-speed=TYPE         帯域幅を TYPE で出力します。TYPE は 'bits' が指定できます。
  -i,  --input-file=FILE           FILE の中に指定された URL をダウンロードする
  -F,  --force-html                入力ファイルを HTML として扱う
  -B,  --base=URL                  HTML で入力されたファイル(-i -F)のリンクを
                                   指定した URL の相対 URL として扱う
       --config=FILE               設定ファイルを指定する
       --no-config                 設定ファイルを読みこまない
       --rejected-log=FILE         拒否された理由をログ FILE に保存する

ダウンロード:
  -t,  --tries=NUMBER              リトライ回数の上限を指定 (0 は無制限).
       --retry-connrefused         接続を拒否されてもリトライする
  -O,  --output-document=FILE      FILE に文書を書きこむ
  -nc, --no-clobber                存在しているファイルをダウンロードで上書きしない
       --no-netrc                  don't try to obtain credentials from .netrc
  -c,  --continue                  部分的にダウンロードしたファイルの続きから始める
       --start-pos=OFFSET          OFFSET からダウンロードを開始する
       --progress=TYPE             進行表示ゲージの種類を TYPE に指定する
       --show-progress             どのモードでも進捗バーを表示する
  -N,  --timestamping              ローカルにあるファイルよりも新しいファイルだけ取得する
       --no-if-modified-since      タイムスタンプモードの時に、
                                     if-modified-since get リクエストを使わない
       --no-use-server-timestamps       ローカル側のファイルのタイムスタンプに
                                   サーバのものを使わない
  -S,  --server-response           サーバの応答を表示する
       --spider                    何もダウンロードしない
  -T,  --timeout=SECONDS           全てのタイムアウトを SECONDS 秒に設定する
       --dns-timeout=SECS          DNS 問い合わせのタイムアウトを SECS 秒に設定する
       --connect-timeout=SECS      接続タイムアウトを SECS 秒に設定する
       --read-timeout=SECS         読み込みタイムアウトを SECS 秒に設定する
  -w,  --wait=SECONDS              ダウンロード毎に SECONDS 秒待つ
       --waitretry=SECONDS         リトライ毎に 1〜SECONDS 秒待つ
       --random-wait               ダウンロード毎に 0.5*WAIT〜1.5*WAIT 秒待つ
       --no-proxy                  プロクシを使わない
  -Q,  --quota=NUMBER              ダウンロードするバイト数の上限を指定する
       --bind-address=ADDRESS      ローカルアドレスとして ADDRESS (ホスト名か IP) を使う
       --limit-rate=RATE           ダウンロード速度を RATE に制限する
       --no-dns-cache              DNS の問い合わせ結果をキャッシュしない
       --restrict-file-names=OS    OS が許しているファイル名に制限する
       --ignore-case               ファイル名/ディレクトリ名の比較で大文字小文字を無視する
  -4,  --inet4-only                IPv4 だけを使う
  -6,  --inet6-only                IPv6 だけを使う
       --prefer-family=FAMILY      指定したファミリ(IPv6, IPv4, none)で最初に接続する
       --user=USER                 ftp, http のユーザ名を指定する
       --password=PASS             ftp, http のパスワードを指定する
       --ask-password              パスワードを別途入力する
       --use-askpass=COMMAND       認証情報(ユーザ名とパスワード)を取得するハンドラを指定します。
                                     COMMAND が指定されない場合は、
                                     環境変数 WGET_ASKPASS か SSH_ASKPASS が
                                     使われます。
       --no-iri                    IRI サポートを使わない
       --local-encoding=ENC        指定した ENC を IRI のローカルエンコーディングにする
       --remote-encoding=ENC       指定した ENC をデフォルトのリモートエンコーディングにする
       --unlink                    上書きする前にファイルを削除する
       --no-xattr                  拡張ファイル属性へのメタデータ保存を無効にする

ディレクトリ:
  -nd, --no-directories            ディレクトリを作らない
  -x,  --force-directories         ディレクトリを強制的に作る
  -nH, --no-host-directories       ホスト名のディレクトリを作らない
       --protocol-directories      プロトコル名のディレクトリを作る
  -P,  --directory-prefix=PREFIX   ファイルを PREFIX/ 以下に保存する
       --cut-dirs=NUMBER           リモートディレクトリ名の NUMBER 階層分を無視する

HTTP オプション:
       --http-user=USER            http ユーザ名として USER を使う
       --http-password=PASS        http パスワードとして PASS を使う
       --no-cache                  サーバがキャッシュしたデータを許可しない
       --default-page=NAME         デフォルトのページ名を NAME に変更します
                                   通常は `index.html' です
  -E,  --adjust-extension          HTML/CSS 文書は適切な拡張子で保存する
       --ignore-length             `Content-Length' ヘッダを無視する
       --header=STRING             送信するヘッダに STRING を追加する
       --max-redirect              ページで許可する最大転送回数
       --proxy-user=USER           プロクシユーザ名として USER を使う
       --proxy-password=PASS       プロクシパスワードとして PASS を使う
       --referer=URL               Referer を URL に設定する
       --save-headers              HTTP のヘッダをファイルに保存する
  -U,  --user-agent=AGENT          User-Agent として Wget/VERSION ではなく AGENT を使う
       --no-http-keep-alive        HTTP の keep-alive (持続的接続) 機能を使わない
       --no-cookies                クッキーを使わない
       --load-cookies=FILE         クッキーを FILE から読みこむ
       --save-cookies=FILE         クッキーを FILE に保存する
       --keep-session-cookies      セッションだけで用いるクッキーを保持する
       --post-data=STRING          POST メソッドを用いて STRING を送信する
       --post-file=FILE            POST メソッドを用いて FILE の中味を送信する
       --method=HTTPMethod         "HTTPMethod" をヘッダのメソッドとして使います
       --body-data=STRING          STRING をデータとして送る。--method を指定してください。
       --body-file=FILE            ファイルの中味を送る。--method を指定してください。
       --content-disposition       Content-Disposition ヘッダがあれば
                                   ローカルのファイル名として用いる (実験的)
       --content-on-error          サーバエラー時に受信した内容を出力する
       --auth-no-challenge         サーバからのチャレンジを待たずに、
                                   Basic認証の情報を送信します。

HTTPS (SSL/TLS) オプション:
       --secure-protocol=PR        choose secure protocol, one of auto, SSLv2,
                                     SSLv3, TLSv1, TLSv1_1, TLSv1_2 and PFS
       --https-only                安全な HTTPS のリンクだけたどる
       --no-check-certificate      サーバ証明書を検証しない
       --certificate=FILE          クライアント証明書として FILE を使う
       --certificate-type=TYPE     クライアント証明書の種類を TYPE (PEM, DER) に設定する
       --private-key=FILE          秘密鍵として FILE を使う
       --private-key-type=TYPE     秘密鍵の種類を TYPE (PEM, DER) に設定する
       --ca-certificate=FILE       CA 証明書として FILE を使う
       --ca-directory=DIR          CA のハッシュリストが保持されているディレクトリを指定する
       --crl-file=FILE             CRL ファイルを指定する
       --pinnedpubkey=FILE/HASHES  公開鍵 (PEM/DER) ファイル、もしくは、base64でエンコードした
                                   sha256ハッシュ値(sha256//で始まりセミコロン区切り)を指定して、
                                   相手を認証します。
       --random-file=FILE          SSL PRNG の初期化データに使うファイルを指定する

HSTS オプション:
       --no-hsts                   HSTS を使わない
       --hsts-file                 HSTS データベースのパス (デフォルトを上書き)

FTP オプション:
       --ftp-user=USER             ftp ユーザとして USER を使う
       --ftp-password=PASS         ftp パスワードとして PASS を使う
       --no-remove-listing         `.listing' ファイルを削除しない
       --no-glob                   FTP ファイル名のグロブを無効にする
       --no-passive-ftp            "passive" 転送モードを使わない
       --preserve-permissions      リモートのファイルパーミッションを保存する
       --retr-symlinks             再帰取得中に、シンボリックリンクでリンクされた先のファイルを取得する

FTPS オプション:
       --ftps-implicit                 implicit FTPS を使う (デフォルトポートは 990)
       --ftps-resume-ssl               制御接続で開始した SSL/TLS セッションを
                                         データ接続で再開する
       --ftps-clear-data-connection    制御チャネルだけ暗号化する(データは平文になる)
       --ftps-fallback-to-ftp          サーバが FTPS に対応していない場合は FTP にする
WARC オプション:
       --warc-file=FILENAME        リクエスト/レスポンスデータを .warc.gz ファイルに保存する
       --warc-header=STRING        warcinfo record に STRING を追加する
       --warc-max-size=NUMBER      WARC ファイルのサイズの最大値を NUMBER に設定する
       --warc-cdx                  CDX インデックスファイルを書く
       --warc-dedup=FILENAME       指定した CDX ファイルに載っている record は保存しない
       --no-warc-digests           SHA1 ダイジェストを計算しない
       --no-warc-keep-log          WARC record にログファイルを保存しない
       --warc-tempdir=DIRECTORY    WARC 書込時の一時ファイルを置くディレクトリを指定する

再帰ダウンロード:
  -r,  --recursive                 再帰ダウンロードを行う
  -l,  --level=NUMBER              再帰時の階層の最大の深さを NUMBER に設定する (0 で無制限)
       --delete-after              ダウンロード終了後、ダウンロードしたファイルを削除する
  -k,  --convert-links             HTML や CSS 中のリンクをローカルを指すように変更する
       --convert-file-only         URLのファイル名部分だけ変換する (いわゆるbasename)
       --backups=N                      ファイルに書きこむ時に N ファイルのバックアップをローテーションさせる
  -K,  --backup-converted          リンク変換前のファイルを .orig として保存する
  -m,  --mirror                    -N -r -l 0 --no-remove-listing の省略形
  -p,  --page-requisites           HTML を表示するのに必要な全ての画像等も取得する
       --strict-comments           HTML 中のコメントの処理を厳密にする

再帰ダウンロード時のフィルタ:
  -A,  --accept=LIST               ダウンロードする拡張子をコンマ区切りで指定する
  -R,  --reject=LIST               ダウンロードしない拡張子をコンマ区切りで指定する
       --accept-regex=REGEX        許容する URL の正規表現を指定する
       --reject-regex=REGEX        拒否する URL の正規表現を指定する
       --regex-type=TYPE           正規表現のタイプ (posix|pcre)
  -D,  --domains=LIST              ダウンロードするドメインをコンマ区切りで指定する
       --exclude-domains=LIST      ダウンロードしないドメインをコンマ区切りで指定する
       --follow-ftp                HTML 文書中の FTP リンクも取得対象にする
       --follow-tags=LIST          取得対象にするタグ名をコンマ区切りで指定する
       --ignore-tags=LIST          取得対象にしないタグ名をコンマ区切りで指定する
  -H,  --span-hosts                再帰中に別のホストもダウンロード対象にする
  -L,  --relative                  相対リンクだけ取得対象にする
  -I,  --include-directories=LIST  取得対象にするディレクトリを指定する
       --trust-server-names             ファイル名としてリダイレクト先のURLの最後の部分を使う
  -X,  --exclude-directories=LIST  取得対象にしないディレクトリを指定する
  -np, --no-parent                 親ディレクトリを取得対象にしない
  ```
