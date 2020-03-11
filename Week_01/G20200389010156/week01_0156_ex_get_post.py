import requests

# GET请求
get_r = requests.get('http://httpbin.org/get')
# print(get_r.headers)
# print(get_r.text)
print(get_r.json())


# POST请求
payload = {'key1': 'value1', 'key2': 'value2'}
post_r = requests.post('http://httpbin.org/post', data = payload)
# print(post_r.text)
print(post_r.json())
