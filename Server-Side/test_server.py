import requests

print('\n')
print(requests.get('http://127.0.0.1:8000').json())
print('\n')
print(requests.get('http://127.0.0.1:8000/player/1').json())