import os
import time

import requests
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

login_url = 'https://tapi.thuhole.com/v3/security/login/login?&device=0&v=v3.0.6-450340'
login_data = {
    'email': 'yinzk19@mails.tsinghua.edu.cn',
    'password_hashed': '2faf6b4382511f9a304e3b15b2aa7e64dbb38aa642aed5bb84b360d8739a7104',
    'device_type': '0',
    'device_info': 'Chrome',
}

session = requests.Session()
login_response = session.post(url=login_url, headers=headers, data=login_data)

token = login_response.json()['token']
list_url = 'https://tapi.thuhole.com/v3/contents/post/list?page=1&device=0&v=v3.0.6-450340'

token_headers = {
    'token': token,
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

list_params = {
    'page': '1',
    'device': '0',
    'v': 'v3.0.6-450340',
}
#list_response = session.get(url=list_url, headers=token_headers, params=list_params)
img_list = []
i = 1
for page in range(1, 2):

    search_url = 'https://tapi.thuhole.com/v3/contents/search'
    search_params = {
        'pagesize': '50',
        'page': str(i),
        'keywords': 'NSFW',
        'device': '0',
        'v': 'v3.0.6-450340',
    }
    search_response = session.get(url=search_url, headers=token_headers, params=search_params)
    img_data = search_response.json()['data']
    for data in img_data:
        url = data['url']
        if url != '':
            img_list.append(url)
    #print(img_list)
    i += 1
    time.sleep(2)

#print(len(img_list))
dir_name = 'thuhole_20210602'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

with open('./' + dir_name + '/url.txt', 'w', encoding='utf-8') as a:
    for img in img_list:
        a.write(img)
for i in range(len(img_list)):
    with open(dir_name + '/' + str(i) + '.' + img_list[i].split('.')[-1], 'wb') as f:
        img_response = requests.get(url='https://i.thuhole.com/' + img_list[i], headers=headers)
        f.write(img_response.content)


