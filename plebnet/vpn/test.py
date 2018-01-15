import json, requests

r = requests.post('https://api.anti-captcha.com/getBalance', json={"clientKey": "fd58e13e22604e820052b44611d61d6c"})

print(r.status_code, r.reason)
print(r.text)
