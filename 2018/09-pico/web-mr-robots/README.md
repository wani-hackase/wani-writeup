# PicoCTF 2018 "Mr. Robots"

<http://2018shell.picoctf.com:15298>

There is no hints in html code.

But, "robots" seems to mean "robots.txt".

Robots.txt is a standard used by websites to communicate with web crawlers and other web robots.

<http://2018shell.picoctf.com:15298/robots.txt>

```
User-agent: *
Disallow: /c4075.html
```

<http://2018shell.picoctf.com:15298/c4075.html>

I get flag picoCTF{th3_w0rld_1s_4_danger0us_pl4c3_3lli0t_c4075}.

There may be hints in robots.txt or sitemap.xml on web problem.
