import	json
import	jwt
import	os

from	falcon			import HTTP_400, HTTP_403, HTTP_500

from	lib.cryption    import	cryptKey

def setAuth(response, client_id, client_secret, level="cliente"):
	try:
		hash	= cryptKey.newKey()
		secret	= cryptKey.encryptContent(client_secret, hash)
		data	= {
			"client_id"		: client_id,
			"hash"			: hash,
			"level"			: level
		}
		save(data, "auth.json")
		return secret
	except Exception:
		response.status = HTTP_500
		return { "error": "unexpected_exception" }

def getAuth(response, client_id, client_secret):
	"""Verify if the login exists"""
	try:
		data_logins	= load("login.json")
		data_auths	= load("auth.json")

		for auth in data_auths:
			if auth['client_id'] == client_id:
				for login in data_logins:
					if login['client_id'] == client_id:
						if client_secret == cryptKey.decryptContent(login['client_secret'], auth['hash']):
							return auth['level']
		return False
	except Exception:
		return False

def getToken(response, grant_type, client_id, client_secret):
	"""Returns a token for an existing client"""
	if grant_type == "client_credentials":
		secret_key	= getSecret()

		level	= getAuth(response, client_id, client_secret)
		if level:
			return {
				"access_token": jwt.encode({
							"client_id"	: client_id,
							"level"		: level
						}, secret_key, algorithm='HS256'
					).decode('utf8'),
				"token_type": "bearer",
			}
		response.status	= HTTP_400
		return { "error": "invalid_client" }
	response.status	= HTTP_400
	return { "error": "unsupported_grant_type" }

def getSecret():
	if not os.path.exists('./.cache'):
		os.makedirs('./.cache')
	if os.path.exists('./.cache/secret.json'):
		with open('./.cache/secret.json', mode='rb') as privatefile:
			return	json.loads(privatefile.read())['secret']
	else:
		with open('./.cache/secret.json', mode='w') as file:
			file.write(json.dumps({ "secret" : cryptKey.newKey() }))
		getSecret()


def save(data, fileName):
	file		= open("./.cache/" + fileName, "r+")
	file_open	= file.read()
	if (isJSON(file_open)):
		content	= json.loads(file_open)
	else:
		content	= []
	content.append(data)
	file.close()
	open("./.cache/"  + fileName, "w").close()
	file	= open("./.cache/"  + fileName, "r+")
	file.write(json.dumps(content))
	file.close()

def load(fileName):
	if not os.path.exists('./.cache'):
		os.makedirs('./.cache')
	if os.path.exists('./.cache/' + fileName):
		with open('./.cache/' + fileName, mode='rb') as read_file:
			return	json.load(read_file)
	else:
		with open('./.cache/' + fileName, mode='w') as write_file:
			write_file.write(json.dumps([]))
		load(fileName)

def isJSON(file):
	try:
		json_object = json.loads(file)
	except:
		return False
	return True