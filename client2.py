import requests

response = requests.post('http://127.0.0.1:5001/advertisement', json={'header': 'job', 'descriptions': 'super',
                                                                      'owner': '1'})


# response = requests.get('http://127.0.0.1:5001/advertisement/1')
#
# print(response.status_code)
# print(response.json())

# response = requests.patch('http://127.0.0.1:5001/advertisement/1', json={'description': 'Oleg'})
#
#
# print(response.status_code)
# print(response.json())

# response = requests.get('http://127.0.0.1:5001/advertisement/1')
#
# print(response.status_code)
# print(response.json())

# response = requests.delete('http://127.0.0.1:5001/advertisement/1')
#
# print(response.status_code)
# print(response.json())
#
# response = requests.get('http://127.0.0.1:5001/advertisement/1')
#
# print(response.status_code)
# print(response.json())