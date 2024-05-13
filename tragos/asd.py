import requests

cookies = {
    'sNdOIy': 'qkeUJMPwIEAoCnaFfOruWBpyYsSTcZ',
    'cookie_id': '524409947cookie_id6641b9c8a0e04',
    'host_name': 'tragos.ru',
    '_ga': 'GA1.1.1249311112.1715583433',
    '_ym_uid': '1715583276790850989',
    '_ym_d': '1715583434',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'PHPSESSID': '575bf1152d54d87f6a4cf32e38f4dfba',
    'qkeUJMPwIEAoCnaFfOruWBpyYsSTcZ': 'bde7538c5cbc3366adb3d110ccd36209-1715583465-1715583459',
    '_ga_17NFE2NVJR': 'GS1.1.1715583433.1.1.1715583951.0.0.0',
    'sNdOIy_hits': '31',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'sNdOIy=qkeUJMPwIEAoCnaFfOruWBpyYsSTcZ; cookie_id=524409947cookie_id6641b9c8a0e04; host_name=tragos.ru; _ga=GA1.1.1249311112.1715583433; _ym_uid=1715583276790850989; _ym_d=1715583434; _ym_isad=2; _ym_visorc=w; PHPSESSID=575bf1152d54d87f6a4cf32e38f4dfba; qkeUJMPwIEAoCnaFfOruWBpyYsSTcZ=bde7538c5cbc3366adb3d110ccd36209-1715583465-1715583459; _ga_17NFE2NVJR=GS1.1.1715583433.1.1.1715583951.0.0.0; sNdOIy_hits=31',
    'Origin': 'https://tragos.ru',
    'Referer': 'https://tragos.ru/alignment-for-the-year/?day=4&month=6&year=2018&age=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

data = {
    'task': 'alignment-for-the-year',
    'day': '4',
    'month': '6',
    'year': '2018',
    'age': '',
}

response = requests.post('https://tragos.ru/tragos_ajax', cookies=cookies, headers=headers, data=data)

print(response.text)