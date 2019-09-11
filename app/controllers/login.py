import	requests

def login(username, password):
	try:
		response	= requests.request('POST', 'http://localhost:8000/oauth/token', data={
			"grant_type": "client_credentials",
			"client_id": username,
			"client_secret": password
		})
		return response.content
	except Exception as e:
		print(e)

# requests.request('POST', "localhost:8000/medias", files={'upload_file': open('file.txt','rb')})