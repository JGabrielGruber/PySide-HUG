import	requests

from	models.login	import Login

def getToken():
	try:
		response	= requests.request('POST', 'http://localhost:8000/oauth/token', data={
			"grant_type": "client_credentials",
			"client_id": Login.client_id,
			"client_secret": Login.client_secret
		})
		content		= eval(response.content)
		if response.status_code == 200:
			Login.setToken(content["access_token"])
			return
		else:
			return content["error"]
	except Exception:
		return "Unexpected error"

# requests.request('POST', "localhost:8000/medias", files={'upload_file': open('file.txt','rb')})