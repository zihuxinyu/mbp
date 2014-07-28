import requests

url = 'http://sso.portal.unicom.local/eip_sso/rest/authentication/login'
values = {
    'return': 'http://www.portal.unicom.local/',
    'success': 'http://www.portal.unicom.local/user/token',
    'error': 'http://www.portal.unicom.local/user/error',
    'appid': 'np000',
    'login': "weibh",
    'password': "wbh12ddddd3!!"

}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
    "Accept": "*/*",
    "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://www.sd.unicom.local:9080/inquiry/login11.jsp",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"

}
r = requests.post(url, data=values, headers=headers)
print(r.text)