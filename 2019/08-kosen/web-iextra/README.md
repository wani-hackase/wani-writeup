# InterKosenCTF "Image Extractor" writeup

## Challenge

```
My hated friend releases a service which extracts images from a document. I want to break it to read /flag.
```

## Solution

docx ファイルをアップロードすると内部の画像ファイルを取り出してくれるサービス

そしてサーバー内の /flag を読み出すとフラグを得られる

> docx ファイルは zip ファイルでそのまま解凍すると word/media ディレクトリ内にドキュメント内の画像が保存されている

ソースコードが与えられるので main.rb を読んでいく

- アップロード部分

```ruby
files = `zipinfo -1 #{filename}`
raise "ERROR" if files.lines.grep(/^word\/media\//).empty?
```

アップロードしたファイルの中に word/media ディレクトリがあることをチェックし、zip ファイルのまま workdir / (hash).zip に保存

- 表示部分

```ruby
@images = `zipinfo -1 #{zipfile}`.lines.grep(/^word\/media\/[A-Za-z0-9_]+\.[A-Za-z0-9_]+/).map do |path|
  path.delete_prefix("word/media/")
```

zip の word/media ディレクトリ内のファイルを表示

- ダウンロード部分

```ruby
zipfile = File.join("workdir", params[:name] + ".zip")
filedir = File.join("workdir", SecureRandom.hex(16))
file = File.join(filedir, params[:image])
system("unzip -j #{zipfile} word/media/#{params[:image]} -d #{filedir}")
if File.exists?(file)
  send_file(file)
```

word/media の中から指定されたファイル名を探し、解凍してダウンロードする

実装的にディレクトリトラバーサルは難しそうなのでシンボリックリンクで /flag を読み出す

```
ln -s /flag test.b
```

上記コマンドで作成した test.b を word/media ディレクトリに入れ zip 化し、docx ファイルにしてアップロードする。そしてサービスから test.b をダウンロードするとフラグが含まれている
