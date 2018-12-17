import requests

url = 'https://api.ipify.org/'
my_ip = requests.get(url, headers=headers).text

print(my_ip)
